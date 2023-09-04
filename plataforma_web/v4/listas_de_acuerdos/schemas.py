"""
Listas de Acuerdos v4, esquemas de pydantic
"""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ListaDeAcuerdoIn(BaseModel):
    """Esquema para recibir una lista de acuerdo"""

    autoridad_id: int | None = None
    fecha: date | None = None
    descripcion: str | None = None
    archivo: str | None = None
    url: str | None = None
    descargar_url: str | None = None


class ListaDeAcuerdoOut(ListaDeAcuerdoIn):
    """Esquema para entregar listas de acuerdos"""

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


class OneListaDeAcuerdoOut(ListaDeAcuerdoOut, OneBaseOut):
    """Esquema para entregar una lista de acuerdo"""
