# NoteResponse

Note as returned by POST /notes/ and GET /notes/

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 
**content** | **str** |  | 
**created_at** | **datetime** |  | 
**tags** | [**List[TagResponse]**](TagResponse.md) |  | 

## Example

```python
from openapi_client.models.note_response import NoteResponse

# TODO update the JSON string below
json = "{}"
# create an instance of NoteResponse from a JSON string
note_response_instance = NoteResponse.from_json(json)
# print the JSON string representation of the object
print(NoteResponse.to_json())

# convert the object into a dict
note_response_dict = note_response_instance.to_dict()
# create an instance of NoteResponse from a dict
note_response_from_dict = NoteResponse.from_dict(note_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


