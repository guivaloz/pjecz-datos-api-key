"""
Listas de Acuerdos v4, rutas (paths)
"""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.listas_de_acuerdos.models import ListaDeAcuerdo
from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import (
    create_lista_de_acuerdo,
    delete_lista_de_acuerdo,
    elaborate_daily_report_listas_de_acuerdos,
    get_lista_de_acuerdo,
    get_listas_de_acuerdos,
    update_lista_de_acuerdo,
)
from .schemas import ListaDeAcuerdoIn, ListaDeAcuerdoOut, OneListaDeAcuerdoOut

listas_de_acuerdos = APIRouter(prefix="/v4/listas_de_acuerdos", tags=["listas de acuerdos"])


@listas_de_acuerdos.get("", response_model=CustomPage[ListaDeAcuerdoOut])
async def paginado_listas_de_acuerdos(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
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
):
    """Paginado de listas de acuerdos"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_listas_de_acuerdos(
            database=database,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            anio=anio,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@listas_de_acuerdos.get("/reporte_diario", response_model=CustomList[ListaDeAcuerdoOut])
async def reporte_diario_listas_de_acuerdos(
    creado: date,
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Reporte diario de listas de acuerdos"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = elaborate_daily_report_listas_de_acuerdos(database, creado)
    except MyAnyError as error:
        return CustomList(success=False, message=str(error))
    if not resultados:
        return CustomList(success=True, message="No hay listas de acuerdos creadas en la fecha indicada", total=0)
    return CustomList(
        success=True,
        message="Sucess",
        total=len(resultados),
        items=resultados,
        page=1,
        size=len(resultados),
        pages=1,
    )


@listas_de_acuerdos.get("/{lista_de_acuerdo_id}", response_model=OneListaDeAcuerdoOut)
async def detalle_lista_de_acuerdo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    lista_de_acuerdo_id: int,
):
    """Detalle de una lista de acuerdo a partir de su id"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        lista_de_acuerdo = get_lista_de_acuerdo(database, lista_de_acuerdo_id)
    except MyAnyError as error:
        return OneListaDeAcuerdoOut(success=False, message=str(error))
    return OneListaDeAcuerdoOut.model_validate(lista_de_acuerdo)


@listas_de_acuerdos.post("", response_model=OneListaDeAcuerdoOut)
async def crear_lista_de_acuerdo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    lista_de_acuerdo_in: ListaDeAcuerdoIn,
):
    """Crear una lista de acuerdo"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        lista_de_acuerdo = create_lista_de_acuerdo(database, ListaDeAcuerdo(**lista_de_acuerdo_in.model_dump()))
    except MyAnyError as error:
        return OneListaDeAcuerdoOut(success=False, message=str(error))
    respuesta = OneListaDeAcuerdoOut.model_validate(lista_de_acuerdo)
    respuesta.message = "Lista de acuerdo creada correctamente"
    return respuesta


@listas_de_acuerdos.put("/{lista_de_acuerdo_id}", response_model=OneListaDeAcuerdoOut)
async def modificar_lista_de_acuerdo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    lista_de_acuerdo_id: int,
    lista_de_acuerdo_in: ListaDeAcuerdoIn,
):
    """Modificar una lista de acuerdo"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.MODIFICAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        lista_de_acuerdo = update_lista_de_acuerdo(
            database, lista_de_acuerdo_id, ListaDeAcuerdo(**lista_de_acuerdo_in.model_dump())
        )
    except MyAnyError as error:
        return OneListaDeAcuerdoOut(success=False, message=str(error))
    respuesta = OneListaDeAcuerdoOut.model_validate(lista_de_acuerdo)
    respuesta.message = "Lista de acuerdo modificada correctamente"
    return respuesta


@listas_de_acuerdos.delete("/{lista_de_acuerdo_id}", response_model=OneListaDeAcuerdoOut)
async def borrar_lista_de_acuerdo(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    lista_de_acuerdo_id: int,
):
    """Borrar una lista de acuerdo"""
    if current_user.permissions.get("LISTAS DE ACUERDOS", 0) < Permiso.BORRAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        lista_de_acuerdo = delete_lista_de_acuerdo(database, lista_de_acuerdo_id)
    except MyAnyError as error:
        return OneListaDeAcuerdoOut(success=False, message=str(error))
    respuesta = OneListaDeAcuerdoOut.model_validate(lista_de_acuerdo)
    respuesta.message = "Lista de Acuerdo borrada correctamente"
    return respuesta
