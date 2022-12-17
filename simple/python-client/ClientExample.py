from caila_gate.CailaClientSDK import CailaClientSDK

# You should specify env variables CAILA_URL and CAILA_TOKEN before run
sdk = CailaClientSDK()
sdk.init()
res = sdk.invoke("1000542", "test", "\"hello\"")
print(res.predict.data.json)
