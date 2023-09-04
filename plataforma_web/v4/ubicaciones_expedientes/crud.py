"""
Ubicaciones de Expedientes v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_expediente

from ...core.ubicaciones_expedientes.models import UbicacionExpediente
from ..autoridades.crud import get_autoridad, get_autoridad_with_clave


def get_ubicaciones_expedientes(
    database: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    expediente: str = None,
) -> Any:
    """Consultar las ubicaciones de expedientes activas"""
    consulta = database.query(UbicacionExpediente)
    if autoridad_id is not None:
        autoridad = get_autoridad(database, autoridad_id)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    elif autoridad_clave is not None:
        autoridad = get_autoridad_with_clave(database, autoridad_clave)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(UbicacionExpediente.creado >= desde_dt).filter(UbicacionExpediente.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        consulta = consulta.filter(UbicacionExpediente.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(UbicacionExpediente.creado <= hasta_dt)
    if expediente is not None:
        try:
            expediente = safe_expediente(expediente)
        except (IndexError, ValueError) as error:
            raise MyNotValidParamError("El expediente no es válido") from error
        consulta = consulta.filter_by(expediente=expediente)
    return consulta.filter_by(estatus="A").order_by(UbicacionExpediente.id.desc())


def get_ubicacion_expediente(database: Session, ubicacion_expediente_id: int) -> UbicacionExpediente:
    """Consultar una ubicacion de expediente por su id"""
    ubicacion_expediente = database.query(UbicacionExpediente).get(ubicacion_expediente_id)
    if ubicacion_expediente is None:
        raise MyNotExistsError("No existe ese ubicacion de expediente")
    if ubicacion_expediente.estatus != "A":
        raise MyIsDeletedError("No es activo ese ubicacion de expediente, está eliminado")
    return ubicacion_expediente
