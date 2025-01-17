# app/auth/document.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..db import Base
from ..auth.models import User  # Importamos User aquí para la FK

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    file_name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_public = Column(Boolean, default=False)

    # Relación con usuario (no va a generar ciclo
    # si 'User' no importa 'Document' a su vez).
    owner = relationship("User", backref="documents")
