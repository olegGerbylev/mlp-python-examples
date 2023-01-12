import json

from caila_gate.openapi_client.apis.tags import account_endpoint_api
from caila_gate.openapi_client.apis.tags import model_endpoint_api
from caila_gate.openapi_client.paths.api_cailagate_account_account_id_model.get import RequestQueryParams, \
    RequestHeaderParams, RequestPathParams
from caila_gate.openapi_client.paths.api_cailagate_account_s3_account_id.get import \
    RequestHeaderParams as S3RequestHeaderParams, RequestPathParams as S3RequestPathParams
from mpl_api import ApiClient, Configuration


def get_api_client():
    configuration = Configuration(host='https://mlp-host')
    configuration.verify_ssl = False
    return ApiClient(configuration=configuration,
                     header_name="MLP-API-KEY",
                     header_value="10.17.HsL0hDyx9gDmsTuLtd81kLnTZht")


if __name__ == "__main__":
    client = get_api_client()

    model_api = model_endpoint_api.ModelEndpointApi(client)
    models_response = model_api.get_paged_models(query_params=RequestQueryParams(),
                                                 header_params=RequestHeaderParams(),
                                                 path_params=RequestPathParams(dict(accountId=1000210)),
                                                 skip_deserialization=True)
    models = json.loads(models_response.response.data)
    print(models["content"][1]["id"]["accountId"])


    account_api = account_endpoint_api.AccountEndpointApi(api_client=client)
    credentials_response = account_api.get_s3_credentials(header_params=S3RequestHeaderParams(),
                                                          path_params=S3RequestPathParams(dict(accountId=1000210)),
                                                          skip_deserialization=True)
    credentials = json.loads(credentials_response.response.data)
    print(credentials["bucketName"])
