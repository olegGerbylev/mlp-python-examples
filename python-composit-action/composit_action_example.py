from mlp_sdk.abstract import Task
from mlp_sdk.hosting.host import host_mlp_cloud
from mlp_sdk.transport.MlpServiceSDK import MlpServiceSDK
from pydantic import BaseModel


class CompositeActionRequest(BaseModel):
    data: str

    def __init__(self, data):
        self.data = data


class CompositeActionResponse(BaseModel):
    value: str

    def __int__(self, value):
        self.value = value


class PunctuationPayload(BaseModel):
    text: str

    def __int__(self, text):
        self.text = text


ACCOUNT = "your_account"
GRAMMAR_MODEL = "your_text_model"
PUNCTUATION_MODEL = "your_punctuation_model"


class CompositActionExample(Task):

    def __init__(self, config: BaseModel, service_sdk: MlpServiceSDK = None) -> None:
        super().__init__(config, service_sdk)

    def predict(self, data: CompositeActionRequest, config: BaseModel) -> CompositeActionResponse:
        grammarModelResponse = self.pipeline_client.predict(account=ACCOUNT, model=GRAMMAR_MODEL, data=data,
                                                            config=config)
        punctuationModelResponse = self.pipeline_client.predict(account=ACCOUNT, model=PUNCTUATION_MODEL,
                                                                data=grammarModelResponse, config=config)
        return CompositeActionResponse(value=punctuationModelResponse.data)


if __name__ == "__main__":
    host_mlp_cloud(CompositActionExample, BaseModel())
