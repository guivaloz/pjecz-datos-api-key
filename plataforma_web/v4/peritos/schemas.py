"""
Peritos v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class PeritoOut(BaseModel):
    """Esquema para entregar peritos"""

    id: int | None = None
    distrito_id: int | None = None
    distrito_clave: str | None = None
    distrito_nombre: str | None = None
    distrito_nombre_corto: str | None = None
    perito_tipo_id: int | None = None
    perito_tipo_nombre: str | None = None
    nombre: str | None = None
    domicilio: str | None = None
    telefono_fijo: str | None = None
    telefono_celular: str | None = None
    email: str | None = None
    notas: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OnePeritoOut(PeritoOut, OneBaseOut):
    """Esquema para entregar un perito"""
