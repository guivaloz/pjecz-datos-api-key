"""
Autoridades v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave

from ...core.autoridades.models import Autoridad
from ..distritos.crud import get_distrito, get_distrito_with_clave
from ..materias.crud import get_materia, get_materia_with_clave


def get_autoridades(
    database: Session,
    distrito_id: int = None,
    distrito_clave: str = None,
    es_archivo_solicitante: bool = None,
    es_cemasc: bool = None,
    es_creador_glosas: bool = None,
    es_defensoria: bool = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    materia_id: int = None,
    materia_clave: str = None,
) -> Any:
    """Consultar los autoridades activos"""
    consulta = database.query(Autoridad)
    if distrito_id is not None:
        distrito = get_distrito(database, distrito_id)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    elif distrito_clave is not None:
        distrito = get_distrito_with_clave(database, distrito_clave)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    if es_archivo_solicitante is not None:
        consulta = consulta.filter_by(es_archivo_solicitante=es_archivo_solicitante)
    if es_cemasc is not None:
        consulta = consulta.filter_by(es_cemasc=es_cemasc)
    if es_creador_glosas is True:
        consulta = consulta.filter(
            Autoridad.organo_jurisdiccional.in_(["PLENO O SALA DEL TSJ", "TRIBUNAL DE CONCILIACION Y ARBITRAJE"])
        )
    if es_defensoria is not None:
        consulta = consulta.filter_by(es_defensoria=es_defensoria)
    if es_jurisdiccional is not None:
        consulta = consulta.filter_by(es_jurisdiccional=es_jurisdiccional)
    if es_notaria is not None:
        consulta = consulta.filter_by(es_notaria=es_notaria)
    if materia_id is not None:
        materia = get_materia(database, materia_id)
        consulta = consulta.filter_by(materia_id=materia.id)
    elif materia_clave is not None:
        materia = get_materia_with_clave(database, materia_clave)
        consulta = consulta.filter_by(materia_id=materia.id)
    return consulta.filter_by(estatus="A").order_by(Autoridad.clave)


def get_autoridad(database: Session, autoridad_id: int) -> Autoridad:
    """Consultar un autoridad por su id"""
    autoridad = database.query(Autoridad).get(autoridad_id)
    if autoridad is None:
        raise MyNotExistsError("No existe ese autoridad")
    if autoridad.estatus != "A":
        raise MyIsDeletedError("No es activo ese autoridad, está eliminado")
    return autoridad


def get_autoridad_with_clave(database: Session, autoridad_clave: str) -> Autoridad:
    """Consultar un autoridad por su clave"""
    try:
        clave = safe_clave(autoridad_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    autoridad = database.query(Autoridad).filter_by(clave=clave).first()
    if autoridad is None:
        raise MyNotExistsError("No existe ese autoridad")
    if autoridad.estatus != "A":
        raise MyIsDeletedError("No es activo ese autoridad, está eliminado")
    return autoridad
