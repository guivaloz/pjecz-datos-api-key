"""
Audiencias v4, esquemas de pydantic
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class AudienciaIn(BaseModel):
    """Esquema para recibir un audiencia"""

    autoridad_id: int | None = None
    tiempo: datetime | None = None
    tipo_audiencia: str | None = None
    expediente: str | None = None
    actores: str | None = None
    demandados: str | None = None
    sala: str | None = None
    caracter: str | None = None
    causa_penal: str | None = None
    delitos: str | None = None
    toca: str | None = None
    expediente_origen: str | None = None
    imputados: str | None = None
    origen: str | None = None


class AudienciaOut(AudienciaIn):
    """Esquema para entregar audiencias"""

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


class OneAudienciaOut(AudienciaOut, OneBaseOut):
    """Esquema para entregar un audiencia"""
