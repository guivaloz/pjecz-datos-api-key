"""
Audiencias v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.audiencias.models import Audiencia
from ...core.autoridades.models import Autoridad
from ..autoridades.crud import get_autoridad, get_autoridad_with_clave
from ..distritos.crud import get_distrito, get_distrito_with_clave


def get_audiencias(
    database: Session,
    anio: int = None,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
) -> Any:
    """Consultar las audiencias activas"""
    consulta = database.query(Audiencia)
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
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(Audiencia.creado >= desde_dt).filter(Audiencia.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        consulta = consulta.filter(Audiencia.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(Audiencia.creado <= hasta_dt)
    if anio is not None:
        desde = datetime(year=anio, month=1, day=1, hour=0, minute=0, second=0)
        hasta = datetime(year=anio, month=12, day=31, hour=23, minute=59, second=59)
        consulta = consulta.filter(Audiencia.tiempo >= desde).filter(Audiencia.tiempo <= hasta)
    elif fecha is not None:
        desde = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=0, minute=0, second=0)
        hasta = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(Audiencia.tiempo >= desde).filter(Audiencia.tiempo <= hasta)
    else:
        if fecha_desde is not None:
            desde = datetime(year=anio, month=1, day=1, hour=0, minute=0, second=0)
            consulta = consulta.filter(Audiencia.tiempo >= desde)
        if fecha_hasta is not None:
            hasta = datetime(year=anio, month=12, day=31, hour=23, minute=59, second=59)
            consulta = consulta.filter(Audiencia.tiempo <= hasta)
    return consulta.filter_by(estatus="A").order_by(Audiencia.id.desc())


def get_audiencia(database: Session, audiencia_id: int) -> Audiencia:
    """Consultar una audiencia por su id"""
    audiencia = database.query(Audiencia).get(audiencia_id)
    if audiencia is None:
        raise MyNotExistsError("No existe esa audiencia")
    if audiencia.estatus != "A":
        raise MyIsDeletedError("No es activa ese audiencia, está eliminada")
    return audiencia


def create_audiencia(database: Session, audiencia: Audiencia) -> Audiencia:
    """Crear una audiencia"""

    # Validar autoridad
    get_autoridad(database, audiencia.autoridad_id)

    # Guardar
    database.add(audiencia)
    database.commit()
    database.refresh(audiencia)

    # Entregar
    return audiencia


def update_audiencia(database: Session, audiencia_id: int, audiencia_in: Audiencia) -> Audiencia:
    """Modificar una audiencia"""

    # Consultar audiencia
    audiencia = get_audiencia(database, audiencia_id)

    # Validar autoridad, si se especificó y se cambió
    if audiencia_in.autoridad_id is not None and audiencia.autoridad_id != audiencia_in.autoridad_id:
        autoridad = get_autoridad(database, audiencia_in.autoridad_id)
        audiencia.autoridad_id = autoridad.autoridad_id

    # Actualizar las columnas
    audiencia.tiempo = audiencia_in.tiempo
    audiencia.tipo_audiencia = audiencia_in.tipo_audiencia
    audiencia.expediente = audiencia_in.expediente
    audiencia.actores = audiencia_in.actores
    audiencia.demandados = audiencia_in.demandados
    audiencia.sala = audiencia_in.sala
    audiencia.caracter = audiencia_in.caracter
    audiencia.causa_penal = audiencia_in.causa_penal
    audiencia.delitos = audiencia_in.delitos
    audiencia.toca = audiencia_in.toca
    audiencia.expediente_origen = audiencia_in.expediente_origen
    audiencia.imputados = audiencia_in.imputados
    audiencia.origen = audiencia_in.origen

    # Guardar
    database.add(audiencia)
    database.commit()
    database.refresh(audiencia)

    # Entregar
    return audiencia


def delete_audiencia(database: Session, audiencia_id: int) -> Audiencia:
    """Borrar una audiencia"""
    audiencia = get_audiencia(database, audiencia_id)
    audiencia.estatus = "B"
    database.add(audiencia)
    database.commit()
    database.refresh(audiencia)
    return audiencia
