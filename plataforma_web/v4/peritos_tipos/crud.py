"""
Peritos - Tipos v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.peritos_tipos.models import PeritoTipo


def get_peritos_tipos(database: Session) -> Any:
    """Consultar los tipos de peritos activos"""
    return database.query(PeritoTipo).filter_by(estatus="A").order_by(PeritoTipo.nombre)


def get_perito_tipo(database: Session, perito_tipo_id: int) -> PeritoTipo:
    """Consultar un tipo de perito por su id"""
    perito_tipo = database.query(PeritoTipo).get(perito_tipo_id)
    if perito_tipo is None:
        raise MyNotExistsError("No existe ese tipo de perito")
    if perito_tipo.estatus != "A":
        raise MyIsDeletedError("No es activo ese tipo de perito, está eliminado")
    return perito_tipo
