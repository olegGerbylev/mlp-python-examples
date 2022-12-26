from typing import Type

from pydantic import BaseModel

from mpl_sdk.abstract import Task
from mpl_sdk.transport.MplActionSDK import PipelineClient, MplActionSDK


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

    def __init__(self, pipeline_client: PipelineClient, config: BaseModel):
        self.pipeline_client = pipeline_client

    @property
    def init_config_schema(self) -> Type[BaseModel]:
        return BaseModel

    def predict(self, data: CompositeActionRequest, config: BaseModel) -> CompositeActionResponse:
        grammarModelResponse = self.pipeline_client.predict(account=ACCOUNT, model=GRAMMAR_MODEL, data=data,
                                                            config=config)
        punctuationModelResponse = self.pipeline_client.predict(account=ACCOUNT, model=PUNCTUATION_MODEL,
                                                                data=grammarModelResponse, config=config)
        return CompositeActionResponse(value=punctuationModelResponse.data)


if __name__ == "__main__":
    sdk = MplActionSDK()
    sdk.register_impl(CompositActionExample(sdk.pipeline_client, BaseModel()))
    sdk.start()
    sdk.block_until_shutdown()
