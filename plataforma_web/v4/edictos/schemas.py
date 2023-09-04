"""
Edictos v4, esquemas de pydantic
"""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class EdictoIn(BaseModel):
    """Esquema para recibir un edicto"""

    autoridad_id: int | None = None
    fecha: date | None = None
    descripcion: str | None = None
    expediente: str | None = None
    numero_publicacion: str | None = None
    archivo: str | None = None
    url: str | None = None
    descargar_url: str | None = None


class EdictoOut(EdictoIn):
    """Esquema para entregar edictos"""

    id: int | None = None
    distrito_id: int | None = None
    distrito_clave: str | None = None
    distrito_nombre: str | None = None
    distrito_nombre_corto: str | None = None
    autoridad_clave: str | None = None
    autoridad_descripcion: str | None = None
    autoridad_descripcion_corta: str | None = None
    creado: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class OneEdictoOut(EdictoOut, OneBaseOut):
    """Esquema para entregar un edicto"""
