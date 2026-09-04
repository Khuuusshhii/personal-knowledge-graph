# NoteDetailResponse

Full note detail as returned by GET /notes/{note_id}. Includes both outgoing links (notes this note points to) and backlinks (notes that point to this note).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 
**content** | **str** |  | 
**created_at** | **datetime** |  | 
**tags** | [**List[TagResponse]**](TagResponse.md) |  | 
**outgoing_links** | [**List[NoteSummary]**](NoteSummary.md) |  | 
**backlinks** | [**List[NoteSummary]**](NoteSummary.md) |  | 

## Example

```python
from openapi_client.models.note_detail_response import NoteDetailResponse

# TODO update the JSON string below
json = "{}"
# create an instance of NoteDetailResponse from a JSON string
note_detail_response_instance = NoteDetailResponse.from_json(json)
# print the JSON string representation of the object
print(NoteDetailResponse.to_json())

# convert the object into a dict
note_detail_response_dict = note_detail_response_instance.to_dict()
# create an instance of NoteDetailResponse from a dict
note_detail_response_from_dict = NoteDetailResponse.from_dict(note_detail_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


