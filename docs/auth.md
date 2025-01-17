Many features in Write API can be controlled through an HTTP-based Application Program Interface (API). All requests must be authenticated using an API key.

## Obtaining an API key
In order to call the Write API, you need an API key. A user can obtain an API key by creating a new account via endpoint.
The holder of an API key can do anything the user can do. However, users with admin privileges have the option of creating API 
keys that have limited permissions. For example, the user could create an API key that only has the permissions of access_user_info 
and create_user, and then use this API key for an integration involving the automatic creation of user accounts. Security would be increased because if the API key was compromised, 
the API key could not be used for accessing the Configuration or installing packages.

## Authentication
To authenticate with the API, you need to provide an bearer token. Pass the Token in the headers as a “bearer token” using the Authorization header, where you prefix the API key with the word Bearer:
The best approach is to send the API key in the headers.

You can send the Token in an HTTP header called Authorization:

``` curl
curl -H "Authorization: Bearer H3PLMKJKIVATLDPWHJH3AGWEJPFU5GRT" http://localhost/document-templates/contrato_idse_pro/parameters
```
In Python, you can set the Authorization by passing a headers dictionary to your requests method:
```bash
import sys
import requests
headers = {'Authorization': 'Bearer H3PLMKJKIVATLDPWHJH3AGWEJPFU5GRT'}

r = requests.get('http://localhost/document-templates/contrato_idse_pro/parameters', headers=headers)
if r.status_code != 200:
sys.exit(r.text)
info = r.json()
```
traditionally the token bearer method expire after a period of time, so using Write API as “bearer tokens” is somewhat of a misnomer. However, passing a token as a “bearer token” is more of an accepted standard than using X-API-Key as a header, so you may find it easier to use the “bearer token” method of authentication.

## Responses
For nearly all API endpoints, the output returned is in JSON format. For example, the output of calling /document-templates/contrato_idse_pro/parameters will look something like this:
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

## Calling POST endpoints
When making a POST request, the data in the request must be passed in the body of the request, not as URL parameters. If the Content-Type header is not set, Write API assumes that the body of the POST request contains data in the standard form data (application/x-www-form-urlencoded or multipart/form-data) format.

For example, to make a POST request using cURL, you can use form data to send the parameters:
``` curl
curl --location 'http://localhost:8007/document-templates/contrato_idse_pro/generate' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzM3MDkxNjU3fQ.Q5KxltB8kr5zvDCffw-hD4fK8MCzOvSGJmGZR792nC0' \
--data '{
  "usuario": "Juan Pérez",
  "razon_social": "COCA COLA COMPANY S.A. DE C.V.",
  "fecha": "Jueves, 16 de enero de 2025"
}'
```
The recommended approach, however, is to always use JSON when sending POST requests instead of sending form data. Many POST API endpoints require several parameters, and it is easy to send these parameters in the form of a JSON object. To do this, set the content type of the request is application/json, and set the body of the POST request to a JSON-formatted object, such as:

{"key": "H3PLMKJKIVATLDPWHJH3AGWEJPFU5GRT", "first_name": "John", "last_name": "Smith"}
The requests module has a convenient built-in feature for sending JSON requests:

It is much easier to send the data parameters as a single JSON object than to use form data, especially when you are using an endpoint like /api/session, where the parameter variables is an object and the parameter delete_variables is an array. When using form data, you would have to do:

The only time you cannot use the JSON Content-Type is when you are making a POST request that includes a file upload. In this circumstance, the format of the POST body cannot be JSON, but must be the traditional multipart/form-data format in which text parameters are provided along with file contents, with boundary separators.