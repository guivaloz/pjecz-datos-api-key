"""
Ubicaciones de Expedientes v4, rutas (paths)
"""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ...core.ubicaciones_expedientes.models import UbicacionExpediente
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import (
    create_ubicacion_expediente,
    delete_ubicacion_expediente,
    get_ubicacion_expediente,
    get_ubicaciones_expedientes,
    update_ubicacion_expediente,
)
from .schemas import OneUbicacionExpedienteOut, UbicacionExpedienteIn, UbicacionExpedienteOut

ubicaciones_expedientes = APIRouter(prefix="/v4/ubicaciones_expedientes", tags=["ubicaciones de expedientes"])


@ubicaciones_expedientes.get("", response_model=CustomPage[UbicacionExpedienteOut])
async def paginado_ubicaciones_expedientes(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    expediente: str = None,
):
    """Paginado de ubicaciones de expedientes"""
    if current_user.permissions.get("UBICACIONES EXPEDIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_ubicaciones_expedientes(
            database=database,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            expediente=expediente,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@ubicaciones_expedientes.get("/{ubicacion_expediente_id}", response_model=OneUbicacionExpedienteOut)
async def detalle_ubicacion_expediente(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    ubicacion_expediente_id: int,
):
    """Detalle de una ubicacion de expediente a partir de su id"""
    if current_user.permissions.get("UBICACIONES EXPEDIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        ubicacion_expediente = get_ubicacion_expediente(database, ubicacion_expediente_id)
    except MyAnyError as error:
        return OneUbicacionExpedienteOut(success=False, message=str(error))
    return OneUbicacionExpedienteOut.model_validate(ubicacion_expediente)


@ubicaciones_expedientes.post("", response_model=OneUbicacionExpedienteOut)
async def crear_ubicacion_expediente(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    ubicacion_expediente_in: UbicacionExpedienteIn,
):
    """Crear una ubicacion de expediente"""
    if current_user.permissions.get("UBICACIONES EXPEDIENTES", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        ubicacion_expediente = create_ubicacion_expediente(
            database, UbicacionExpediente(**ubicacion_expediente_in.model_dump())
        )
    except MyAnyError as error:
        return OneUbicacionExpedienteOut(success=False, message=str(error))
    respuesta = OneUbicacionExpedienteOut.model_validate(ubicacion_expediente)
    respuesta.message = "Ubicacion de expediente creada correctamente"
    return respuesta


@ubicaciones_expedientes.put("/{ubicacion_expediente_id}", response_model=OneUbicacionExpedienteOut)
async def modificar_ubicacion_expediente(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    ubicacion_expediente_id: int,
    ubicacion_expediente_in: UbicacionExpedienteIn,
):
    """Modificar una ubicacion de expediente"""
    if current_user.permissions.get("UBICACIONES EXPEDIENTES", 0) < Permiso.MODIFICAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        ubicacion_expediente = update_ubicacion_expediente(
            database, ubicacion_expediente_id, UbicacionExpediente(**ubicacion_expediente_in.model_dump())
        )
    except MyAnyError as error:
        return OneUbicacionExpedienteOut(success=False, message=str(error))
    respuesta = OneUbicacionExpedienteOut.model_validate(ubicacion_expediente)
    respuesta.message = "Ubicacion expediente modificada correctamente"
    return respuesta


@ubicaciones_expedientes.delete("/{ubicacion_expediente_id}", response_model=OneUbicacionExpedienteOut)
async def borrar_ubicacion_expediente(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    ubicacion_expediente_id: int,
):
    """Borrar una ubicacion de expediente"""
    if current_user.permissions.get("UBICACIONES EXPEDIENTES", 0) < Permiso.BORRAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        ubicacion_expediente = delete_ubicacion_expediente(database, ubicacion_expediente_id)
    except MyAnyError as error:
        return OneUbicacionExpedienteOut(success=False, message=str(error))
    respuesta = OneUbicacionExpedienteOut.model_validate(ubicacion_expediente)
    respuesta.message = "Ubicacion expediente borrada correctamente"
    return respuesta
