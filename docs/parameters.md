## Extract fields from a template file

Description: Returns information about the field names used in a PDF, DOCX, or Markdown file.

Path: /document-templates/{template_id}/parameters

### Method: GET

### Data:

- template_id: a template file id that exist on Write API.

### Responses on failure:

- 403 “Access Denied” if the API key did not authenticate.
- 400 “Invalid output format” if the format is not json or yaml.
- 400 “File not included.” if a file is not uploaded.
- 400 “No fields could be found.” if the format is yaml and no fields could be detected in the file.

Response on success: 200

Body of response: a JSON list of field information, or a YAML draft question, depending on the requested format.

The JSON output for the file sample-form.pdf looks like this:
```json
[
  {
    "name": "usuario",
    "type": "string",
    "required": true
  },
  {
    "name": "fecha",
    "type": "string",
    "required": true
  },
  {
    "name": "razon_social",
    "type": "string",
    "required": true
  }
]
```