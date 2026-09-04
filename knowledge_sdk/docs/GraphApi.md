# openapi_client.GraphApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_graph_graph_get**](GraphApi.md#get_graph_graph_get) | **GET** /graph/ | Get Graph


# **get_graph_graph_get**
> GraphResponse get_graph_graph_get()

Get Graph

Return the entire knowledge graph as a set of nodes and edges.

- nodes: every note, represented as { id, title }
- edges: every link, represented as { source_id, target_id }

The frontend uses this data to render a text-based graph map.
Advanced visualisation libraries (e.g. D3, Cytoscape) can also
consume this format.

### Example


```python
import openapi_client
from openapi_client.models.graph_response import GraphResponse
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
    api_instance = openapi_client.GraphApi(api_client)

    try:
        # Get Graph
        api_response = api_instance.get_graph_graph_get()
        print("The response of GraphApi->get_graph_graph_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GraphApi->get_graph_graph_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GraphResponse**](GraphResponse.md)

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

