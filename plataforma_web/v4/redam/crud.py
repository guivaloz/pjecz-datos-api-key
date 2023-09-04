"""
REDAM (Registro Estatal de Deudores Alimentarios Morosos) v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_expediente, safe_string

from ...core.autoridades.models import Autoridad
from ...core.redam.models import Redam
from ..autoridades.crud import get_autoridad, get_autoridad_with_clave
from ..distritos.crud import get_distrito, get_distrito_with_clave


def get_redams(
    database: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    nombre: str = None,
    expediente: str = None,
) -> Any:
    """Consultar los deudores alimenticios morosos activos"""
    consulta = database.query(Redam)
    if autoridad_id is not None:
        autoridad = get_autoridad(database, autoridad_id)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    elif autoridad_clave is not None:
        autoridad = get_autoridad_with_clave(database, autoridad_clave)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    elif distrito_id is not None:
        distrito = get_distrito(database, distrito_id)
        consulta = consulta.join(Autoridad).filter(Autoridad.distrito_id == distrito.id)
    elif distrito_clave is not None:
        distrito = get_distrito_with_clave(database, distrito_clave)
        consulta = consulta.join(Autoridad).filter(Autoridad.distrito_id == distrito.id)
    if nombre is not None:
        nombre = safe_string(nombre)
        if nombre == "":
            raise MyNotValidParamError("El nombre no es válido")
        consulta = consulta.filter(Redam.nombre.contains(nombre))
    if expediente is not None:
        try:
            expediente = safe_expediente(expediente)
        except (IndexError, ValueError) as error:
            raise MyNotValidParamError("El expediente no es válido") from error
        consulta = consulta.filter_by(expediente=expediente)
    return consulta.filter_by(estatus="A").order_by(Redam.nombre)


def get_redam(database: Session, redam_id: int) -> Redam:
    """Consultar un deudor alimenticio moroso por su id"""
    redam = database.query(Redam).get(redam_id)
    if redam is None:
        raise MyNotExistsError("No existe ese redam")
    if redam.estatus != "A":
        raise MyIsDeletedError("No es activo ese redam, está eliminado")
    return redam
