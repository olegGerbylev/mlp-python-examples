from mlp_sdk.abstract import Task
from mlp_sdk.hosting.host import host_mlp_cloud
from mlp_sdk.transport.MlpServiceSDK import MlpServiceSDK
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

    def __init__(self, config: BaseModel, service_sdk: MlpServiceSDK = None) -> None:
        super().__init__(config, service_sdk)

    def predict(self, data: PredictRequest, config: BaseModel) -> PredictResponse:
        if data.action == 'predict':
            return PredictResponse(value='hello ' + data.name)
        raise ValueError('action not found')


if __name__ == "__main__":
    host_mlp_cloud(SimpleActionExample, BaseModel())
