"""
REPSVM Agresores v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class RepsvmAgresorOut(BaseModel):
    """Esquema para entregar agresores"""

    id: int | None = None
    distrito_id: int | None = None
    distrito_clave: str | None = None
    distrito_nombre: str | None = None
    distrito_nombre_corto: str | None = None
    consecutivo: int | None = None
    delito_generico: str | None = None
    delito_especifico: str | None = None
    nombre: str | None = None
    numero_causa: str | None = None
    pena_impuesta: str | None = None
    observaciones: str | None = None
    sentencia_url: str | None = None
    tipo_juzgado: str | None = None
    tipo_sentencia: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneRepsvmAgresorOut(RepsvmAgresorOut, OneBaseOut):
    """Esquema para entregar un agresor"""
