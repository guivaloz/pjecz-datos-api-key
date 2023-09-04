"""
Materias v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class MateriaListOut(BaseModel):
    """Esquema para entregar materias"""

    id: int | None = None
    clave: str | None = None
    nombre: str | None = None
    en_sentencias: bool | None = None
    model_config = ConfigDict(from_attributes=True)


class MateriaOut(MateriaListOut):
    """Esquema para entregar materias"""


class OneMateriaOut(MateriaOut, OneBaseOut):
    """Esquema para entregar una materia"""
