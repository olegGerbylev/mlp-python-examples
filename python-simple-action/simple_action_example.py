from typing import Type

from mpl_sdk.abstract import Task
from mpl_sdk.transport.MplActionSDK import MplActionSDK
from pydantic import BaseModel


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
    sdk = MplActionSDK()
    sdk.register_impl(SimpleActionExample(BaseModel()))
    sdk.start()
    sdk.block_until_shutdown()
