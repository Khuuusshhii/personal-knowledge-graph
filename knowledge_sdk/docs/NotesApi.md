# openapi_client.NotesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_note_notes_post**](NotesApi.md#create_note_notes_post) | **POST** /notes/ | Create Note
[**get_note_notes_note_id_get**](NotesApi.md#get_note_notes_note_id_get) | **GET** /notes/{note_id} | Get Note
[**link_notes_notes_note_id_link_patch**](NotesApi.md#link_notes_notes_note_id_link_patch) | **PATCH** /notes/{note_id}/link | Link Notes
[**list_all_tags_notes_tags_all_get**](NotesApi.md#list_all_tags_notes_tags_all_get) | **GET** /notes/tags/all | List All Tags
[**list_notes_notes_get**](NotesApi.md#list_notes_notes_get) | **GET** /notes/ | List Notes


# **create_note_notes_post**
> NoteResponse create_note_notes_post(note_create)

Create Note

Create a new note with a title, content, and optional tags.

Business logic that runs automatically:
  - Tags are normalised (stripped and lowercased) before being saved.
  - The content is scanned for [[Note Title]] patterns; any titles that
    match an existing note are automatically turned into outgoing links.

### Example


```python
import openapi_client
from openapi_client.models.note_create import NoteCreate
from openapi_client.models.note_response import NoteResponse
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
    api_instance = openapi_client.NotesApi(api_client)
    note_create = openapi_client.NoteCreate() # NoteCreate | 

    try:
        # Create Note
        api_response = api_instance.create_note_notes_post(note_create)
        print("The response of NotesApi->create_note_notes_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->create_note_notes_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_create** | [**NoteCreate**](NoteCreate.md)|  | 

### Return type

[**NoteResponse**](NoteResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_note_notes_note_id_get**
> NoteDetailResponse get_note_notes_note_id_get(note_id)

Get Note

Return full details for one note, including:
  - outgoing_links: notes that this note links to
  - backlinks:      notes that link TO this note

Backlinks are computed by finding all NoteLinks where target_id == note_id.

### Example


```python
import openapi_client
from openapi_client.models.note_detail_response import NoteDetailResponse
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
    api_instance = openapi_client.NotesApi(api_client)
    note_id = 56 # int | 

    try:
        # Get Note
        api_response = api_instance.get_note_notes_note_id_get(note_id)
        print("The response of NotesApi->get_note_notes_note_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->get_note_notes_note_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**|  | 

### Return type

[**NoteDetailResponse**](NoteDetailResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **link_notes_notes_note_id_link_patch**
> NoteDetailResponse link_notes_notes_note_id_link_patch(note_id, link_create)

Link Notes

Create a manual directed link from note_id → link_data.target_id.

Rules enforced:
  - A note cannot link to itself (self-link prevention).
  - Duplicate links are silently ignored (idempotent — returns the note
    unchanged rather than raising an error, which is friendlier for the UI).
  - Both notes must exist (404 if either is missing).

### Example


```python
import openapi_client
from openapi_client.models.link_create import LinkCreate
from openapi_client.models.note_detail_response import NoteDetailResponse
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
    api_instance = openapi_client.NotesApi(api_client)
    note_id = 56 # int | 
    link_create = openapi_client.LinkCreate() # LinkCreate | 

    try:
        # Link Notes
        api_response = api_instance.link_notes_notes_note_id_link_patch(note_id, link_create)
        print("The response of NotesApi->link_notes_notes_note_id_link_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->link_notes_notes_note_id_link_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**|  | 
 **link_create** | [**LinkCreate**](LinkCreate.md)|  | 

### Return type

[**NoteDetailResponse**](NoteDetailResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

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
    api_instance = openapi_client.NotesApi(api_client)

    try:
        # List All Tags
        api_response = api_instance.list_all_tags_notes_tags_all_get()
        print("The response of NotesApi->list_all_tags_notes_tags_all_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->list_all_tags_notes_tags_all_get: %s\n" % e)
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

# **list_notes_notes_get**
> List[NoteResponse] list_notes_notes_get(tag=tag, keyword=keyword)

List Notes

Return all notes, newest first.

Optional query parameters:
  - ?tag=python     → only notes tagged 'python'
  - ?keyword=graph  → only notes whose title or content contains 'graph'
  - Both filters can be combined (AND logic).

### Example


```python
import openapi_client
from openapi_client.models.note_response import NoteResponse
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
    api_instance = openapi_client.NotesApi(api_client)
    tag = 'tag_example' # str | Filter notes by tag name (optional)
    keyword = 'keyword_example' # str | Filter notes by keyword in title or content (optional)

    try:
        # List Notes
        api_response = api_instance.list_notes_notes_get(tag=tag, keyword=keyword)
        print("The response of NotesApi->list_notes_notes_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->list_notes_notes_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tag** | **str**| Filter notes by tag name | [optional] 
 **keyword** | **str**| Filter notes by keyword in title or content | [optional] 

### Return type

[**List[NoteResponse]**](NoteResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

