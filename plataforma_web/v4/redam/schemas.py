"""
REDAM (Registro Estatal de Deudores Alimentarios Morosos) v4, esquemas de pydantic
"""
from datetime import date

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class RedamOut(BaseModel):
    """Esquema para entregar deudores alimentarios morosos"""

    id: int | None = None
    distrito_id: int | None = None
    distrito_clave: str | None = None
    distrito_nombre: str | None = None
    distrito_nombre_corto: str | None = None
    autoridad_id: int | None = None
    autoridad_clave: str | None = None
    autoridad_descripcion: str | None = None
    autoridad_descripcion_corta: str | None = None
    nombre: str | None = None
    expediente: str | None = None
    fecha: date | None = None
    observaciones: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneRedamOut(RedamOut, OneBaseOut):
    """Esquema para entregar un deudor alimentario moroso"""
