# NoteSummary

Minimal note info — used when listing outgoing links or backlinks.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 

## Example

```python
from openapi_client.models.note_summary import NoteSummary

# TODO update the JSON string below
json = "{}"
# create an instance of NoteSummary from a JSON string
note_summary_instance = NoteSummary.from_json(json)
# print the JSON string representation of the object
print(NoteSummary.to_json())

# convert the object into a dict
note_summary_dict = note_summary_instance.to_dict()
# create an instance of NoteSummary from a dict
note_summary_from_dict = NoteSummary.from_dict(note_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


