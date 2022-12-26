from mpl_sdk.transport.MplClientSDK import MplClientSDK


class PredictRequest:
    action: str
    name: str

    def __init__(self, action, name):
        self.action = action
        self.name = name


ACCOUNT = "your_account"
MODEL = "model_to_invoke_predict"

sdk = MplClientSDK()
sdk.init()
predict_result = sdk.predict(account=ACCOUNT, model=MODEL, data=PredictRequest(action="predict", name="Elon"))
