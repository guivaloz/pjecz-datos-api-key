"""
Glosas v4, esquemas de pydantic
"""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class GlosaIn(BaseModel):
    """Esquema para recibir una glosa"""

    autoridad_id: int | None = None
    fecha: date | None = None
    tipo_juicio: str | None = None
    descripcion: str | None = None
    expediente: str | None = None
    archivo: str | None = None
    url: str | None = None
    descargar_url: str | None = None


class GlosaOut(GlosaIn):
    """Esquema para entregar glosas"""

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


class OneGlosaOut(GlosaOut, OneBaseOut):
    """Esquema para entregar una glosa"""
