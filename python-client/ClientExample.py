from caila_sdk.transport.CailaClientSDK import CailaClientSDK

# You should specify env variables CAILA_URL and CAILA_TOKEN before run
sdk = CailaClientSDK()
sdk.init()
res = sdk.predict("just-ai", "test-action", "\"hello\"")

print(str(res))
