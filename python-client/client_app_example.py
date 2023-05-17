from mlp_sdk.transport.MlpClientSDK import MlpClientSDK
from mlp_sdk.types import TextsCollection

ACCOUNT = "just-ai"
MODEL = "platform-vectorizer-ru-test"

sdk = MlpClientSDK()
sdk.init()
req = TextsCollection(texts=["Hello"])
res = sdk.predict(account=ACCOUNT, model=MODEL, data=req.json())
print(res)
sdk.shutdown()
