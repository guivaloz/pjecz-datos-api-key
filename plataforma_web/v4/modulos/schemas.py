"""
Modulos v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class ModuloListOut(BaseModel):
    """Esquema para entregar modulos"""

    id: int | None = None
    nombre_corto: str | None = None
    model_config = ConfigDict(from_attributes=True)


class ModuloOut(ModuloListOut):
    """Esquema para entregar modulos"""

    nombre: str | None = None
    icono: str | None = None
    ruta: str | None = None
    en_navegacion: bool | None = None


class OneModuloOut(ModuloOut, OneBaseOut):
    """Esquema para entregar un modulo"""
