import pickle
from pathlib import Path
from typing import Union, Type

from pydantic import BaseModel

from mpl_sdk.abstract import Task
from mpl_sdk.hosting.host import host
from mpl_sdk.storage.local_storage import LocalStorage
from mpl_sdk.storage.s3_storage import S3Storage
from mpl_sdk.types import ItemsCollection, TextsCollection
from mpl_sdk.utilities.misc import get_env


class PredictResponse(BaseModel):
    value: str

    def __int__(self, value):
        self.value = value


class PredictRequest(BaseModel):
    image: str

    def __int__(self, image):
        self.image = image


class FitActionExample(Task):

    @property
    def init_config_schema(self) -> Type[BaseModel]:
        return BaseModel

    def get_storage(self, model_dir: str = '') -> Union[LocalStorage, S3Storage]:
        storage_type = get_env('MPL_STORAGE_TYPE')
        storage_dir = get_env('MPL_STORAGE_DIR') if len(model_dir) == 0 else model_dir

        if storage_type == LocalStorage.name():
            storage = LocalStorage(path=Path(storage_dir))

        elif storage_type == S3Storage.name():
            storage = S3Storage(
                bucket=get_env('MPL_S3_BUCKET'),
                data_dir=storage_dir,
                service_name='s3',
                region=get_env('MPL_S3_REGION', ''),
                access_key=get_env('MPL_S3_ACCESS_KEY'),
                secret_key=get_env('MPL_S3_SECRET_KEY'),
                endpoint=get_env('MPL_S3_ENDPOINT'),
            )

        else:
            message = f"storage_type {storage_type} is invalid."
            raise ValueError(message)

        return storage

    def __init__(self, config: BaseModel) -> None:
        super().__init__(config)

        self.storage = self.get_storage()
        self.model_path = 'model.pkl'

        self.is_fitted_model = False

        try:
            self._load_state()
        except KeyError as e:
            print(f'Unable to load saved state, error message: {str(e)}')

    def _fit(
            self,
            train_data: TextsCollection,
            targets: ItemsCollection,
            config: BaseModel,
            model_dir: str,
            previous_model_dir: str,
    ) -> None:
        self.storage = self.get_storage(model_dir)
        self.current_model_dir = model_dir

        num_samples, num_targets = len(train_data.texts), len(targets.items_list)

        if num_samples != num_targets:
            raise ValueError(f'Inconsistent data sizes')

        self.model = FittedMLModel(self._prepareModelData(train_data.texts, targets.items_list))
        self.is_fitted_model = True

    def predict(self, data: PredictRequest, config: BaseModel) -> PredictResponse:
        predict = self.model.predict(data.image)
        return PredictResponse(value=predict)

    def _prepareModelData(self, texts: [str], items_list: [str]):
        data = dict()
        for i in len(texts):
            data[texts[i]] = items_list[i]
        return data

    def _load_state(self):
        with self.storage.open(self.model_path, 'rb') as fin:
            self.model = pickle.loads(fin.read())
        self.is_fitted_model = True


class FittedMLModel:

    def __init__(self, data):
        self.data = data

    def predict(self, number):
        return self.data[number]


if __name__ == "__main__":
    host(FitActionExample, BaseModel(), 5000)
