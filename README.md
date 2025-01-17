# Write API

## Overview
The Write API is a lightweight and scalable microservice designed to streamline the massive generation of documents via API. This project addresses a key challenge in the legal contract signing process for products offered by Apimarket, providing a seamless, automated, and secure solution to generate massive docs.

### Key Features
- **Template-Based Design**: Generate documents from `.docx`, `.md`, or `.html` templates with support for dynamic variable injection using Jinja2.
- **YAML Configuration**: Define logic, structure, and validation rules for templates in YAML format, ensuring consistency and error prevention.
- **Flexible Output Formats**: Supports `.docx` (default), `.pdf`, and `.html` outputs for diverse use cases.
- **Massive Document Generation**: Optimized for high-volume operations, enabling large-scale automated workflows.
- **Authentication**: Secure token-based authentication protects all API endpoints.
- **Lightweight & Customizable**: No GUI ensures a lightweight design, and Docker compatibility enables easy deployment and scalability.
- **Powerful API Ready**: Start using this project right now with the API gateway ready to use.

---

## Deployment Instructions

### Using Docker (Recommended)
The easiest and most reliable way to deploy the Write API is by using Docker. Follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/write-api.git
   cd write-api
   ```

2. **Build the Docker Image**:
   ```bash
   docker-compose build --no-cache
   ```

3. **Start the Service**:
   ```bash
   docker-compose up
   ```

4. **Access the API**:
   The API will be available at `http://localhost:8007`. Adjust the port in the `docker-compose.yml` file if needed.

5. **Stop the Service**:
   To stop the service, run:
   ```bash
   docker-compose down
   ```

---

## Authentication
The Write API uses a secure token-based authentication system to protect its endpoints.

### Obtaining an API Token
1. Sign up using the `/auth/signup` endpoint.
2. Log in with your credentials at `/auth/login` to receive an access token.

### Using the Token
Include the token in the `Authorization` header of your HTTP requests as a Bearer token:

#### Example with `curl`:
```bash
curl -H "Authorization: Bearer <your_api_token>" \
     http://localhost/document-templates/{template_id}/parameters
```

#### Example with Python:
```python
import requests
headers = {'Authorization': 'Bearer <your_api_token>'}
response = requests.get('http://localhost/document-templates/{template_id}/parameters', headers=headers)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.text}")
```

---

## Parameters Section

### Overview
The Parameters Section provides essential details about the inputs required for document generation. These parameters are defined in the YAML configuration associated with each template.

### Structure
Each parameter includes:
- **`name`**: The name of the variable.
- **`type`**: The expected data type (`string`, `int`, `date`, etc.).
- **`required`**: Indicates whether the parameter is mandatory or optional.

#### Example:
```json
[
  {
    "name": "usuario",
    "type": "string",
    "required": true
  },
  {
    "name": "fecha",
    "type": "date",
    "required": true
  }
]
```

### Accessing Parameters
To retrieve the required parameters for a specific template, use the `/document-templates/{template_id}/parameters` endpoint.

---

## Document Generation

### Overview
The **Document Generation Section** enables users to create highly customized documents from predefined templates, leveraging Jinja2 for variable injection.

### Supported Template Formats
- **`.docx`**: Ideal for editable documents.
- **`.md`**: Markdown templates for simple and structured content.
- **`.html`**: Templates for web-based content.

### Variable Format
To ensure variables are recognized by Jinja2, use the following syntax in templates:
```plaintext
{{ variable_name }}
```
#### Example:
```plaintext
Hello, {{ user_name }}! Your contract starts on {{ start_date }}.
```

### YAML Validation
The variables in the template must match those defined in the associated YAML configuration. The API:
1. Validates the input data against the YAML configuration.
2. Ensures all required variables are provided and meet the expected format.
3. Returns an error if any required variable is missing or mismatched.

### Output Formats
- **DOCX**: The default format if none is specified.
- **PDF**: For finalized, non-editable documents.
- **HTML**: Web-based formats when needed.

### Example Requests
#### Generating a Document (JSON Body)
```bash
curl --location 'http://localhost:8007/document-templates/{template_id}/generate' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <your_api_token>' \
--data '{
  "usuario": "Juan Pérez",
  "razon_social": "COCA COLA COMPANY S.A. DE C.V.",
  "fecha": "2025-01-16"
}'
```

---

## Roadmap

### Pending Features
1. **Public URL for Generated Documents**:
    - Generate a public, time-signed cryptographic URL for accessing documents.
    - Ensure time-based expiration for secure access.

2. **Database Integration**:
    - Implement relational database tables to enable scaling as a SaaS.
    - Store relationships between YAML files, templates, and user data.

3. **Upload and Validation Endpoints**:
    - Extend current upload functionality to support uploading templates (`.docx`, `.md`, `.html`).
    - Validate the association between uploaded templates and YAML logic before saving.

4. **Document Retrieval by User**:
    - Create endpoints to retrieve generated documents for each user.
    - Provide access to available templates per user.

5. **Team Features**:
    - Implement functionality for managing teams within the API.
    - Allow team-based access to templates and generated documents.

6. **Unique Token Authentication**:
    - Introduce single-use tokens for simplified integrations.
    - Avoid sharing permanent API keys for enhanced security.
    - Eliminate session renewal requirements for password-based JWT authentication.

7. **Permission Management**:
    - Develop a granular permission system.
    - Define access control for users and tokens, limiting their scope to specific actions or templates.

---

## Contribution
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with detailed changes.

For questions, feel free to create an issue in the repository.

---

## Security Vulnerabilities

If you discover a security vulnerability in Livewirestack, please help us maintain the security of this project by responsibly disclosing it to us. To report a security vulnerability, please send an email to [hh.abdiel@gmail.com](mailto:hh.abdiel@gmail.com). We'll address the issue as promptly as possible.

## Credits

- [Abdiel Hernandez](https://github.com/exonos)

## Support My Work

If you find Livewirestack helpful and would like to support my work, you can buy me a coffee. Your support will help keep this project alive and thriving. It's a small token of appreciation that goes a long way.

[![Buy me a coffee](https://cdn.buymeacoffee.com/buttons/default-orange.png)](https://buymeacoffee.com/exonos)

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.

<br />
<p align="center"> <b>Made with ❤️ from Mexico</b> </p>
