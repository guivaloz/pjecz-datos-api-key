"""
Abogados v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_string

from ...core.abogados.models import Abogado


def get_abogados(
    database: Session,
    nombre: str = None,
    anio_desde: int = None,
    anio_hasta: int = None,
) -> Any:
    """Consultar los abogados activos"""
    consulta = database.query(Abogado)
    if anio_desde is not None:
        if 1925 <= anio_desde <= datetime.now().year:
            consulta = consulta.filter(Abogado.fecha >= date(year=anio_desde, month=1, day=1))
        else:
            raise MyNotValidParamError("Año fuera de rango.")
    if anio_hasta is not None:
        if 1925 <= anio_hasta <= datetime.now().year:
            consulta = consulta.filter(Abogado.fecha <= date(year=anio_hasta, month=12, day=31))
        else:
            raise MyNotValidParamError("Año fuera de rango.")
    if nombre is not None:
        nombre = safe_string(nombre)
        if nombre == "":
            raise MyNotValidParamError("El nombre es incorrecto.")
        consulta = consulta.filter(Abogado.nombre.contains(nombre))
    return consulta.filter_by(estatus="A").order_by(Abogado.id.desc())


def get_abogado(database: Session, abogado_id: int) -> Abogado:
    """Consultar un abogado por su id"""
    abogado = database.query(Abogado).get(abogado_id)
    if abogado is None:
        raise MyNotExistsError("No existe ese abogado")
    if abogado.estatus != "A":
        raise MyIsDeletedError("No es activo ese abogado, está eliminado")
    return abogado


def create_abogado(database: Session, abogado: Abogado) -> Abogado:
    """Crear un abogado"""
    database.add(abogado)
    database.commit()
    database.refresh(abogado)
    return abogado


def update_abogado(database: Session, abogado_id: int, abogado_in: Abogado) -> Abogado:
    """Modificar un abogado"""
    abogado = get_abogado(database, abogado_id)
    abogado.fecha = abogado_in.fecha
    abogado.numero = abogado_in.numero
    abogado.libro = abogado_in.libro
    abogado.nombre = abogado_in.nombre
    database.add(abogado)
    database.commit()
    database.refresh(abogado)
    return abogado


def delete_abogado(database: Session, abogado_id: int) -> Abogado:
    """Borrar un abogado"""
    abogado = get_abogado(database, abogado_id)
    abogado.estatus = "B"
    database.add(abogado)
    database.commit()
    database.refresh(abogado)
    return abogado
