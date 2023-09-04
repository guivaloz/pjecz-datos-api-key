"""
Autoridades v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class AutoridadListOut(BaseModel):
    """Esquema para entregar autoridades como listado"""

    id: int | None = None
    clave: str | None = None
    descripcion_corta: str | None = None
    model_config = ConfigDict(from_attributes=True)


class AutoridadOut(AutoridadListOut):
    """Esquema para entregar autoridades como paginado"""

    distrito_id: int | None = None
    distrito_clave: str | None = None
    distrito_nombre: str | None = None
    distrito_nombre_corto: str | None = None
    materia_id: int | None = None
    materia_clave: str | None = None
    materia_nombre: str | None = None
    descripcion: str | None = None
    es_archivo_solicitante: bool | None = None
    es_cemasc: bool | None = None
    es_creador_glosas: bool | None = None
    es_defensoria: bool | None = None
    es_jurisdiccional: bool | None = None
    es_notaria: bool | None = None
    organo_jurisdiccional: str | None = None
    audiencia_categoria: str | None = None


class OneAutoridadOut(AutoridadOut, OneBaseOut):
    """Esquema para entregar un autoridad"""
