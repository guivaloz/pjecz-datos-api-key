"""
Sentencias v4, esquemas de pydantic
"""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class SentenciaIn(BaseModel):
    """Esquema para recibir una sentencia"""

    autoridad_id: int | None = None
    materia_tipo_juicio_id: int | None = None
    sentencia: str | None = None
    sentencia_fecha: date | None = None
    expediente: str | None = None
    fecha: date | None = None
    descripcion: str | None = None
    es_perspectiva_genero: bool | None = None
    archivo: str | None = None
    url: str | None = None
    descargar_url: str | None = None


class SentenciaOut(SentenciaIn):
    """Esquema para entregar sentencias"""

    id: int | None = None
    distrito_id: int | None = None
    distrito_clave: str | None = None
    distrito_nombre: str | None = None
    distrito_nombre_corto: str | None = None
    autoridad_clave: str | None = None
    autoridad_descripcion: str | None = None
    autoridad_descripcion_corta: str | None = None
    expediente_anio: int | None = None
    expediente_num: int | None = None
    materia_id: int | None = None
    materia_nombre: str | None = None
    materia_tipo_juicio_descripcion: str | None = None
    creado: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class OneSentenciaOut(SentenciaOut, OneBaseOut):
    """Esquema para entregar una sentencia"""
