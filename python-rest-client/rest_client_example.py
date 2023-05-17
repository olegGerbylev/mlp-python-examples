import json

from mlp_sdk.transport.MlpClientSDK import MlpRestClient

ACCOUNT = "just-ai"
MODEL = "test-action"

restClient = MlpRestClient()

# predict
res = restClient.processApi.predict("hello", path_params={'account': ACCOUNT, 'model': MODEL})
print(res.body)

# getModelInfo
# we should use skip_deserialization=True here because of a bug in swagger client generator
res = restClient.modelApi.get_model_info(path_params={'account': ACCOUNT, 'model': MODEL}, skip_deserialization=True)

body = json.loads(res.response.data)
print(body)
print(body['modelName'])
