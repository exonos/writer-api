# app/main.py

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from datetime import timedelta

from .db import Base, engine, SessionLocal
from .auth.services import (
    create_user,
    authenticate_user,
    create_access_token,
    get_current_user,
    UserCreate,
    UserLogin
)
from .auth.models import User
from .models.document import Document
from .services.generator import (
    get_template_parameters,
    generate_document
)

Base.metadata.create_all(bind=engine)  # Crear tablas si no existen

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# Auth endpoints
# ---------------------------
@app.post("/auth/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user_data)
        return {"id": new_user.id, "email": new_user.email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------------------
# Document templates (YAML)
# ---------------------------
@app.post("/document-templates")
async def upload_template(
    template_id: str = Form(...),
    file: UploadFile = File(...),
):
    """
    Sube un archivo YAML y lo guarda con el nombre `{template_id}.yaml`.
    """
    # Ajusta la ruta a tu carpeta de YAML
    import os

    YAML_PATH = "yamls"  # Si está en la raíz de tu proyecto
    if not os.path.exists(YAML_PATH):
        os.makedirs(YAML_PATH)

    if not (file.filename.endswith(".yaml") or file.filename.endswith(".yml")):
        raise HTTPException(status_code=400, detail="El archivo debe tener extensión .yaml o .yml.")

    yaml_file_path = os.path.join(YAML_PATH, f"{template_id}.yaml")
    contents = await file.read()
    with open(yaml_file_path, "wb") as f:
        f.write(contents)

    return {"message": f"YAML '{template_id}' subido con éxito."}


@app.get("/document-templates/{template_id}/parameters")
def read_template_parameters(template_id: str):
    """
    Retorna la lista de parámetros que se requieren
    para generar el documento (definidos en el archivo YAML).
    """
    params = get_template_parameters(template_id)
    return params


# ---------------------------
# Generación de documentos
# ---------------------------
@app.post("/document-templates/{template_id}/generate")
def generate_doc(
    template_id: str,
    request_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Genera un documento usando el template YAML y la información provista.
    Retorna la ruta del archivo generado y su formato.
    """
    try:
        file_path, file_format = generate_document(
            template_id=template_id,
            request_data=request_data,
            db=db,
            current_user_id=current_user.id,
            is_public=False  # o True si deseas permitir
        )
        return {
            "message": "Documento generado con éxito",
            "file_path": file_path,
            "format": file_format
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ejemplo de endpoint protegido
@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hola, {current_user.email}. Tienes acceso a este endpoint protegido."}
