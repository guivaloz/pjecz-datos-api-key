"""
Ubicaciones de Expedientes v4, esquemas de pydantic
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class UbicacionExpedienteIn(BaseModel):
    """Esquema para recibir una ubicacion de expediente"""

    autoridad_id: int | None = None
    expediente: str | None = None
    ubicacion: str | None = None


class UbicacionExpedienteOut(UbicacionExpedienteIn):
    """Esquema para entregar ubicaciones de expedientes"""

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


class OneUbicacionExpedienteOut(UbicacionExpedienteOut, OneBaseOut):
    """Esquema para entregar una ubicacion de expediente"""
