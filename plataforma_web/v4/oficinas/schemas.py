"""
Oficinas v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class OficinaListOut(BaseModel):
    """Esquema para entregar oficinas"""

    id: int | None = None
    clave: str | None = None
    descripcion_corta: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OficinaOut(OficinaListOut):
    """Esquema para entregar oficinas"""

    distrito_id: int | None = None
    distrito_clave: str | None = None
    distrito_nombre: str | None = None
    distrito_nombre_corto: str | None = None
    domicilio_id: int | None = None
    domicilio_completo: str | None = None
    domicilio_edificio: str | None = None
    descripcion: str | None = None
    es_jurisdiccional: bool | None = None


class OneOficinaOut(OficinaOut, OneBaseOut):
    """Esquema para entregar un oficina"""
