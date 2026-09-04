# openapi_client.TagsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_all_tags_notes_tags_all_get**](TagsApi.md#list_all_tags_notes_tags_all_get) | **GET** /notes/tags/all | List All Tags


# **list_all_tags_notes_tags_all_get**
> List[TagResponse] list_all_tags_notes_tags_all_get()

List All Tags

Return every existing tag, alphabetically sorted.
Used by the frontend to populate the tag filter dropdown.

### Example


```python
import openapi_client
from openapi_client.models.tag_response import TagResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.TagsApi(api_client)

    try:
        # List All Tags
        api_response = api_instance.list_all_tags_notes_tags_all_get()
        print("The response of TagsApi->list_all_tags_notes_tags_all_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TagsApi->list_all_tags_notes_tags_all_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[TagResponse]**](TagResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

