"""
Sentencias v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any, List

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import extract_expediente_anio, extract_expediente_num, safe_expediente

from ...core.autoridades.models import Autoridad
from ...core.sentencias.models import Sentencia
from ..autoridades.crud import get_autoridad, get_autoridad_with_clave, get_autoridades
from ..distritos.crud import get_distrito, get_distrito_with_clave
from ..materias_tipos_juicios.crud import get_materia_tipo_juicio


def get_sentencias(
    database: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    expediente_anio: int = None,
    expediente_num: int = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
    materia_tipo_juicio_id: int = None,
    sentencia: str = None,
) -> Any:
    """Consultar los sentencias activos"""
    consulta = database.query(Sentencia)
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
        consulta = consulta.filter(Sentencia.creado >= desde_dt).filter(Sentencia.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        consulta = consulta.filter(Sentencia.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(Sentencia.creado <= hasta_dt)
    if fecha is not None:
        consulta = consulta.filter(Sentencia.fecha == fecha)
    else:
        if fecha_desde is not None:
            consulta = consulta.filter(Sentencia.fecha >= fecha_desde)
        if fecha_hasta is not None:
            consulta = consulta.filter(Sentencia.fecha <= fecha_hasta)
    if expediente_anio is not None:
        consulta = consulta.filter_by(expediente_anio=expediente_anio)
    if expediente_num is not None:
        consulta = consulta.filter_by(expediente_num=expediente_num)
    if materia_tipo_juicio_id is not None:
        materia_tipo_juicio = get_materia_tipo_juicio(database, materia_tipo_juicio_id)
        consulta = consulta.filter_by(materia_tipo_juicio_id=materia_tipo_juicio.id)
    if sentencia is not None:
        try:
            sentencia = safe_expediente(sentencia)
        except (IndexError, ValueError) as error:
            raise MyNotValidParamError("La sentencia no es válida") from error
        consulta = consulta.filter_by(sentencia=sentencia)
    return consulta.filter_by(estatus="A").order_by(Sentencia.id.desc())


def get_sentencia(database: Session, sentencia_id: int) -> Sentencia:
    """Consultar un sentencia por su id"""
    sentencia = database.query(Sentencia).get(sentencia_id)
    if sentencia is None:
        raise MyNotExistsError("No existe ese sentencia")
    if sentencia.estatus != "A":
        raise MyIsDeletedError("No es activo ese sentencia, está eliminado")
    return sentencia


def create_sentencia(database: Session, sentencia: Sentencia) -> Sentencia:
    """Crear una nueva sentencia"""

    # Validar autoridad
    get_autoridad(database, sentencia.autoridad_id)

    # Validar materia_tipo_juicio
    get_materia_tipo_juicio(database, sentencia.materia_tipo_juicio_id)

    # Validar expediente
    try:
        expediente = safe_expediente(sentencia.expediente)
        sentencia.expediente_anio = extract_expediente_anio(expediente)
        sentencia.expediente_num = extract_expediente_num(expediente)
    except (IndexError, ValueError) as error:
        raise MyNotValidParamError("El expediente no es válido") from error

    # Guardar
    database.add(sentencia)
    database.commit()
    database.refresh(sentencia)

    # Entregar
    return sentencia


def update_sentencia(database: Session, sentencia_id: int, sentencia_in: Sentencia) -> Sentencia:
    """Modificar una sentencia"""

    # Consultar la sentencia
    sentencia = get_sentencia(database, sentencia_id)

    # Validad autoridad, si se especificó y es diferente
    if sentencia_in.autoridad_id is not None and sentencia_in.autoridad_id != sentencia.autoridad_id:
        autoridad = get_autoridad(database, sentencia_in.autoridad_id)
        sentencia.autoridad_id = autoridad.id

    # Validad materia_tipo_juicio, si se especificó y es diferente
    if (
        sentencia_in.materia_tipo_juicio_id is not None
        and sentencia_in.materia_tipo_juicio_id != sentencia.materia_tipo_juicio_id
    ):
        materia_tipo_juicio = get_materia_tipo_juicio(database, sentencia_in.materia_tipo_juicio_id)
        sentencia.materia_tipo_juicio_id = materia_tipo_juicio.id

    # Actualizar las columnas
    sentencia.sentencia = sentencia_in.sentencia
    sentencia.sentencia_fecha = sentencia_in.sentencia_fecha
    sentencia.expediente = sentencia_in.expediente
    sentencia.expediente_anio = extract_expediente_anio(sentencia_in.expediente)
    sentencia.expediente_num = extract_expediente_num(sentencia_in.expediente)
    sentencia.fecha = sentencia_in.fecha
    sentencia.descripcion = sentencia_in.descripcion
    sentencia.es_perspectiva_genero = sentencia_in.es_perspectiva_genero
    sentencia.archivo = sentencia_in.archivo
    sentencia.url = sentencia_in.url

    # Guardar
    database.add(sentencia)
    database.commit()
    database.refresh(sentencia)

    # Entregar
    return sentencia


def delete_sentencia(database: Session, sentencia_id: int) -> Sentencia:
    """Borrar una sentencia"""
    sentencia = get_sentencia(database, sentencia_id)
    sentencia.estatus = "B"
    database.add(sentencia)
    database.commit()
    database.refresh(sentencia)
    return sentencia


def elaborate_daily_report_sentencias(
    database: Session,
    creado: date,
) -> List[Sentencia]:
    """Elaborar reporte diario de edictos"""
    resultados = []
    for autoridad in get_autoridades(database=database, es_jurisdiccional=True, es_notaria=False).all():
        existentes = get_sentencias(database=database, autoridad_id=autoridad.id, creado=creado).all()
        if existentes:
            resultados.extend(existentes)
    return resultados
