"""
Materias-Tipos de Juicios v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class MateriaTipoJuicioListOut(BaseModel):
    """Esquema para entregar materias-tipos de juicios"""

    id: int | None = None
    descripcion: str | None = None
    model_config = ConfigDict(from_attributes=True)


class MateriaTipoJuicioOut(MateriaTipoJuicioListOut):
    """Esquema para entregar materias-tipos de juicios"""

    materia_id: int | None = None
    materia_clave: str | None = None
    materia_nombre: str | None = None


class OneMateriaTipoJuicioOut(MateriaTipoJuicioOut, OneBaseOut):
    """Esquema para entregar un materia-tipo de juicio"""
