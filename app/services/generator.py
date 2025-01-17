import os
import uuid
import yaml
import subprocess
from dateutil.parser import parse as parse_date
from docxtpl import DocxTemplate
from jinja2 import Template
import markdown
from weasyprint import HTML
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..auth.document import Document

# Definir rutas base
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # app/
YAML_DIR = os.path.join(BASE_DIR, "yamls")            # app/yamls
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")    # app/templates
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")        # app/outputs

# Crear directorios si no existen
os.makedirs(YAML_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_template_parameters(template_id: str):
    yaml_file = os.path.join(YAML_DIR, f"{template_id}.yaml")
    if not os.path.exists(yaml_file):
        return {"error": f"El template_id '{template_id}' no existe."}

    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data.get("parameters", [])

def generate_document(
    template_id: str,
    request_data: dict,
    db: Session,
    current_user_id: int,
    is_public: bool = False
):
    yaml_file = os.path.join(YAML_DIR, f"{template_id}.yaml")
    if not os.path.exists(yaml_file):
        raise FileNotFoundError(f"El template_id '{template_id}' no existe.")

    with open(yaml_file, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)

    template_name = config_data.get("template_name")
    required_parameters = config_data.get("parameters", [])

    validate_request_data(request_data, required_parameters)

    output_format = request_data.get("format", "docx")  # Por defecto, "docx"

    template_path = os.path.join(TEMPLATE_DIR, template_name)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"No se encontró la plantilla '{template_name}' en '{template_path}'.")

    ext = os.path.splitext(template_name)[1].lower()
    if ext not in [".docx", ".md", ".html"]:
        raise ValueError(f"Formato de plantilla no soportado: {ext}")

    # Generar nombre único para el archivo de salida
    final_ext = ".pdf" if output_format == "pdf" else ext
    output_file_name = generate_unique_filename(template_id, final_ext)
    output_path = os.path.join(OUTPUT_DIR, output_file_name)

    # Lógica para distintos formatos de entrada
    if ext == ".docx":
        intermediate_docx = render_docx(template_path, request_data)

        if output_format == "pdf":
            try:
                pdf_path = convert_docx_to_pdf(intermediate_docx, output_file_name)
                register_document_in_db(db, current_user_id, os.path.basename(pdf_path), is_public)
                return pdf_path, "pdf"
            finally:
                if os.path.exists(intermediate_docx):
                    os.remove(intermediate_docx)
        else:
            register_document_in_db(db, current_user_id, os.path.basename(intermediate_docx), is_public)
            return intermediate_docx, "docx"

    elif ext in [".md", ".html"]:
        with open(template_path, "r", encoding="utf-8") as f:
            template_text = f.read()
        rendered_html = Template(template_text).render(**request_data)

        if output_format == "pdf":
            pdf_file = render_html_to_pdf(rendered_html, output_file_name)
            register_document_in_db(db, current_user_id, os.path.basename(pdf_file), is_public)
            return pdf_file, "pdf"
        else:
            with open(output_path, "w", encoding="utf-8") as out:
                out.write(rendered_html)
            register_document_in_db(db, current_user_id, output_file_name, is_public)
            return output_path, "html"

def validate_request_data(request_data: dict, required_params: list):
    errors = []
    for param in required_params:
        name = param["name"]
        param_type = param.get("type", "string")
        is_required = param.get("required", False)

        if is_required and name not in request_data:
            errors.append(f"Falta el parámetro requerido: '{name}'")
            continue

        if name not in request_data:
            continue

        value = request_data[name]
        if not validate_type(value, param_type):
            errors.append(f"El parámetro '{name}' debe ser de tipo '{param_type}' (recibido: {type(value).__name__}).")

    if errors:
        raise ValueError(" | ".join(errors))

def validate_type(value, expected_type: str) -> bool:
    if expected_type == "string":
        return isinstance(value, str)
    elif expected_type == "int":
        return isinstance(value, int)
    elif expected_type == "float":
        return isinstance(value, float)
    elif expected_type == "bool":
        return isinstance(value, bool)
    elif expected_type == "date":
        if isinstance(value, str):
            try:
                parse_date(value)
                return True
            except:
                return False
        return False
    return True

def generate_unique_filename(template_id: str, ext: str = ".docx") -> str:
    unique_id = str(uuid.uuid4())
    return f"{template_id}_{unique_id}{ext}"

def render_docx(template_path: str, request_data: dict) -> str:
    doc = DocxTemplate(template_path)
    doc.render(request_data)
    temp_file_name = generate_unique_filename("temp_docx", ".docx")
    output_path = os.path.join(OUTPUT_DIR, temp_file_name)
    doc.save(output_path)
    return output_path

def render_html_to_pdf(html_content: str, final_filename: str) -> str:
    pdf_file = os.path.join(OUTPUT_DIR, final_filename)
    HTML(string=html_content).write_pdf(pdf_file)
    return pdf_file

def register_document_in_db(db: Session, user_id: int, file_name: str, is_public: bool = False):
    doc = Document(
        owner_id=user_id,
        file_name=file_name,
        is_public=is_public
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def convert_docx_to_pdf(docx_file: str, final_filename: str) -> str:
    pdf_file = os.path.join(OUTPUT_DIR, final_filename)

    command = [
        "libreoffice",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        OUTPUT_DIR,
        docx_file,
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error al convertir {docx_file} a PDF: {str(e)}")

#     if not os.path.exists(pdf_file):
#         raise FileNotFoundError(f"No se pudo generar el PDF en {pdf_file}")

    os.remove(docx_file)  # Eliminar archivo intermedio DOCX

    return pdf_file
