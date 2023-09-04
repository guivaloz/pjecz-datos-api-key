"""
Listas de Acuerdos v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any, List

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.autoridades.models import Autoridad
from ...core.listas_de_acuerdos.models import ListaDeAcuerdo
from ..autoridades.crud import get_autoridad, get_autoridad_with_clave, get_autoridades
from ..distritos.crud import get_distrito, get_distrito_with_clave


def get_listas_de_acuerdos(
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
    """Consultar los listas de acuerdos activos"""
    consulta = database.query(ListaDeAcuerdo)
    if autoridad_id is not None:
        autoridad = get_autoridad(database, autoridad_id)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    elif autoridad_clave is not None:
        autoridad = get_autoridad_with_clave(database, autoridad_clave)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(ListaDeAcuerdo.creado >= desde_dt).filter(ListaDeAcuerdo.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        consulta = consulta.filter(ListaDeAcuerdo.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(ListaDeAcuerdo.creado <= hasta_dt)
    elif distrito_id is not None:
        distrito = get_distrito(database, distrito_id)
        consulta = consulta.join(Autoridad).filter(Autoridad.distrito_id == distrito.id)
    elif distrito_clave is not None:
        distrito = get_distrito_with_clave(database, distrito_clave)
        consulta = consulta.join(Autoridad).filter(Autoridad.distrito_id == distrito.id)
    if anio is not None:
        desde = date(year=anio, month=1, day=1)
        hasta = date(year=anio, month=12, day=31)
        consulta = consulta.filter(ListaDeAcuerdo.fecha >= desde).filter(ListaDeAcuerdo.fecha <= hasta)
    elif fecha is not None:
        consulta = consulta.filter(ListaDeAcuerdo.fecha == fecha)
    else:
        if fecha_desde is not None:
            consulta = consulta.filter(ListaDeAcuerdo.fecha >= fecha_desde)
        if fecha_hasta is not None:
            consulta = consulta.filter(ListaDeAcuerdo.fecha <= fecha_hasta)
    return consulta.filter_by(estatus="A").order_by(ListaDeAcuerdo.id.desc())


def get_lista_de_acuerdo(
    database: Session,
    lista_de_acuerdo_id: int,
) -> ListaDeAcuerdo:
    """Consultar un lista de acuerdo por su id"""
    lista_de_acuerdo = database.query(ListaDeAcuerdo).get(lista_de_acuerdo_id)
    if lista_de_acuerdo is None:
        raise MyNotExistsError("No existe ese lista de acuerdo")
    if lista_de_acuerdo.estatus != "A":
        raise MyIsDeletedError("No es activo ese lista de acuerdo, está eliminado")
    return lista_de_acuerdo


def create_lista_de_acuerdo(
    database: Session,
    lista_de_acuerdo: ListaDeAcuerdo,
) -> ListaDeAcuerdo:
    """Crear una lista de acuerdos"""

    # Validar autoridad
    get_autoridad(database, lista_de_acuerdo.autoridad_id)

    # Guardar
    database.add(lista_de_acuerdo)
    database.commit()
    database.refresh(lista_de_acuerdo)

    # Entregar
    return lista_de_acuerdo


def update_lista_de_acuerdo(
    database: Session,
    lista_de_acuerdo_id: int,
    lista_de_acuerdo_in: ListaDeAcuerdo,
) -> ListaDeAcuerdo:
    """Modificar una lista de acuerdos"""

    # Consultar lista de acuerdos
    lista_de_acuerdo = get_lista_de_acuerdo(database, lista_de_acuerdo_id)

    # Validar autoridad, si se especificó y se cambió
    if lista_de_acuerdo_in.autoridad_id is not None and lista_de_acuerdo.autoridad_id != lista_de_acuerdo_in.autoridad_id:
        autoridad = get_autoridad(database, lista_de_acuerdo_in.autoridad_id)
        lista_de_acuerdo.autoridad_id = autoridad.autoridad_id

    # Actualizar las columnas
    lista_de_acuerdo.fecha = lista_de_acuerdo_in.fecha
    lista_de_acuerdo.descripcion = lista_de_acuerdo_in.descripcion
    lista_de_acuerdo.archivo = lista_de_acuerdo_in.archivo
    lista_de_acuerdo.url = lista_de_acuerdo_in.url

    # Guardar
    database.add(lista_de_acuerdo)
    database.commit()
    database.refresh(lista_de_acuerdo)

    # Entregar
    return lista_de_acuerdo


def delete_lista_de_acuerdo(
    database: Session,
    lista_de_acuerdo_id: int,
) -> ListaDeAcuerdo:
    """Borrar una lista de acuerdos"""
    lista_de_acuerdo = get_lista_de_acuerdo(database, lista_de_acuerdo_id)
    lista_de_acuerdo.estatus = "B"
    database.add(lista_de_acuerdo)
    database.commit()
    database.refresh(lista_de_acuerdo)
    return lista_de_acuerdo


def elaborate_daily_report_listas_de_acuerdos(
    database: Session,
    creado: date,
) -> List[ListaDeAcuerdo]:
    """Elaborar reporte diario de listas de acuerdos"""
    resultados = []
    for autoridad in get_autoridades(database=database, es_jurisdiccional=True, es_notaria=False).all():
        existentes = get_listas_de_acuerdos(database=database, autoridad_id=autoridad.id, creado=creado).all()
        if existentes:
            resultados.extend(existentes)
        else:
            resultados.append(
                ListaDeAcuerdo(
                    id=0,
                    autoridad_id=autoridad.id,
                    autoridad=autoridad,
                    fecha=creado,
                    descripcion="No se publicó",
                    archivo="",
                    url="",
                    creado=datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0),
                )
            )
    return resultados
