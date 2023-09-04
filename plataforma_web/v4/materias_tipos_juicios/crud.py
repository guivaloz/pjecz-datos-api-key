"""
Materias-Tipos de Juicios v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.materias_tipos_juicios.models import MateriaTipoJuicio
from ..materias.crud import get_materia, get_materia_with_clave


def get_materias_tipos_juicios(
    database: Session,
    materia_id: int = None,
    materia_clave: str = None,
) -> Any:
    """Consultar los materias-tipos de juicios activos"""
    consulta = database.query(MateriaTipoJuicio)
    if materia_id is not None:
        materia = get_materia(database, materia_id)
        consulta = consulta.filter_by(materia_id=materia.id)
    elif materia_clave is not None:
        materia = get_materia_with_clave(database, materia_clave)
        consulta = consulta.filter_by(materia_id=materia.id)
    return consulta.filter_by(estatus="A").order_by(MateriaTipoJuicio.descripcion)


def get_materia_tipo_juicio(database: Session, materia_tipo_juicio_id: int) -> MateriaTipoJuicio:
    """Consultar un materia-tipo de juicio por su id"""
    materia_tipo_juicio = database.query(MateriaTipoJuicio).get(materia_tipo_juicio_id)
    if materia_tipo_juicio is None:
        raise MyNotExistsError("No existe ese materia-tipo de juicio")
    if materia_tipo_juicio.estatus != "A":
        raise MyIsDeletedError("No es activo ese materia-tipo de juicio, está eliminado")
    return materia_tipo_juicio
