from typing import Type

from pydantic import BaseModel

from mpl_sdk.abstract import Task
from mpl_sdk.hosting.host import host


class PredictRequest(BaseModel):
    action: str
    name: str

    def __int__(self, action, name):
        self.action = action
        self.name = name


class PredictResponse(BaseModel):
    value: str

    def __int__(self, value):
        self.value = value


class SimpleActionExample(Task):
    @property
    def init_config_schema(self) -> Type[BaseModel]:
        return BaseModel

    def predict(self, data: PredictRequest, config: BaseModel) -> PredictResponse:
        if data.action == 'predict':
            return PredictResponse(value='hello ' + data.name)
        raise ValueError('action not found')


if __name__ == "__main__":
    host(SimpleActionExample, BaseModel(), 5000)
