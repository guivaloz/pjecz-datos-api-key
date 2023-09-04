"""
REPSVM Agresores v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_string

from ...core.repsvm_agresores.models import RepsvmAgresor
from ..distritos.crud import get_distrito, get_distrito_with_clave


def get_repsvm_agresores(
    database: Session,
    distrito_id: int = None,
    distrito_clave: str = None,
    nombre: str = None,
) -> Any:
    """Consultar los agresores activos"""
    consulta = database.query(RepsvmAgresor)
    if distrito_id is not None:
        distrito = get_distrito(database, distrito_id)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    elif distrito_clave is not None:
        distrito = get_distrito_with_clave(database, distrito_clave)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    if nombre is not None:
        nombre = safe_string(nombre)
        if nombre == "":
            raise MyNotValidParamError("El nombre no es válido")
        consulta = consulta.filter(RepsvmAgresor.nombre.contains(nombre))
    return consulta.filter_by(estatus="A").order_by(RepsvmAgresor.nombre)


def get_repsvm_agresor(database: Session, repsvm_agresor_id: int) -> RepsvmAgresor:
    """Consultar un agresor por su id"""
    repsvm_agresor = database.query(RepsvmAgresor).get(repsvm_agresor_id)
    if repsvm_agresor is None:
        raise MyNotExistsError("No existe ese agresor")
    if repsvm_agresor.estatus != "A":
        raise MyIsDeletedError("No es activo ese agresor, está eliminado")
    return repsvm_agresor
