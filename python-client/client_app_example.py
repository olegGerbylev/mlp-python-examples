from mlp_sdk.transport.MlpClientSDK import MlpClientSDK


class PredictRequest:
    action: str
    name: str

    def __init__(self, action, name):
        self.action = action
        self.name = name


ACCOUNT = "your_account"
MODEL = "model_to_invoke_predict"

sdk = MlpClientSDK()
sdk.init()
predict_result = sdk.predict(account=ACCOUNT, model=MODEL, texts=PredictRequest(action="predict", name="Elon"))
