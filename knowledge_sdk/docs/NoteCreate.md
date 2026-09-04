# NoteCreate

Body for POST /notes/

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**content** | **str** |  | [optional] [default to '']
**tags** | **List[str]** |  | [optional] [default to []]

## Example

```python
from openapi_client.models.note_create import NoteCreate

# TODO update the JSON string below
json = "{}"
# create an instance of NoteCreate from a JSON string
note_create_instance = NoteCreate.from_json(json)
# print the JSON string representation of the object
print(NoteCreate.to_json())

# convert the object into a dict
note_create_dict = note_create_instance.to_dict()
# create an instance of NoteCreate from a dict
note_create_from_dict = NoteCreate.from_dict(note_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


