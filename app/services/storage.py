# app/services/storage.py
import time
import jwt
from datetime import datetime, timedelta
from ..config import SECRET_KEY, ALGORITHM

def generate_signed_url(file_name: str, expires_in: int = 3600):
    """
    Genera un token con info del archivo y la hora de expiración.
    """
    expire = datetime.utcnow() + timedelta(seconds=expires_in)
    payload = {
        "file_name": file_name,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def validate_signed_url(token: str):
    """
    Valida el token y retorna el file_name si es válido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        file_name = payload.get("file_name")
        if not file_name:
            return None
        return file_name
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None
