"""
Domicilios v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class DomicilioListOut(BaseModel):
    """Esquema para entregar domicilios"""

    id: int | None = None
    edificio: str | None = None
    model_config = ConfigDict(from_attributes=True)


class DomicilioOut(DomicilioListOut):
    """Esquema para entregar domicilios"""

    distrito_id: int | None = None
    distrito_clave: str | None = None
    distrito_nombre: str | None = None
    distrito_nombre_corto: str | None = None
    estado: str | None = None
    municipio: str | None = None
    calle: str | None = None
    num_ext: str | None = None
    num_int: str | None = None
    colonia: str | None = None
    cp: int | None = None
    completo: str | None = None


class OneDomicilioOut(DomicilioOut, OneBaseOut):
    """Esquema para entregar un domicilio"""
