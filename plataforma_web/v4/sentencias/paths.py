"""
Sentencias v4, rutas (paths)
"""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ...core.sentencias.models import Sentencia
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import (
    create_sentencia,
    delete_sentencia,
    elaborate_daily_report_sentencias,
    get_sentencia,
    get_sentencias,
    update_sentencia,
)
from .schemas import OneSentenciaOut, SentenciaIn, SentenciaOut

sentencias = APIRouter(prefix="/v4/sentencias", tags=["sentencias"])


@sentencias.get("", response_model=CustomPage[SentenciaOut])
async def paginado_sentencias(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
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
    materia_tipo_juicio_id: int = None,
    sentencia: str = None,
):
    """Paginado de sentencias"""
    if current_user.permissions.get("SENTENCIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_sentencias(
            database=database,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            expediente_anio=expediente_anio,
            expediente_num=expediente_num,
            fecha=fecha,
            materia_tipo_juicio_id=materia_tipo_juicio_id,
            sentencia=sentencia,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@sentencias.get("/reporte_diario", response_model=CustomList[SentenciaOut])
async def reporte_diario_sentencias(
    creado: date,
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Reporte diario de sentencias"""
    if current_user.permissions.get("SENTENCIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = elaborate_daily_report_sentencias(database, creado)
    except MyAnyError as error:
        return CustomList(success=False, message=str(error))
    if not resultados:
        return CustomList(success=True, message="No hay sentencias creadas en la fecha indicada", total=0)
    return CustomList(
        success=True,
        message="Sucess",
        total=len(resultados),
        items=resultados,
        page=1,
        size=len(resultados),
        pages=1,
    )


@sentencias.get("/{sentencia_id}", response_model=OneSentenciaOut)
async def detalle_sentencia(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    sentencia_id: int,
):
    """Detalle de una sentencia a partir de su id"""
    if current_user.permissions.get("SENTENCIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        sentencia = get_sentencia(database, sentencia_id)
    except MyAnyError as error:
        return OneSentenciaOut(success=False, message=str(error))
    return OneSentenciaOut.model_validate(sentencia)


@sentencias.post("", response_model=OneSentenciaOut)
async def crear_sentencia(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    sentencia_in: SentenciaIn,
):
    """Crear una sentencia"""
    if current_user.permissions.get("SENTENCIAS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        sentencia = create_sentencia(database, Sentencia(**sentencia_in.model_dump()))
    except MyAnyError as error:
        return OneSentenciaOut(success=False, message=str(error))
    respuesta = OneSentenciaOut.model_validate(sentencia)
    respuesta.message = "Sentencia creada correctamente"
    return respuesta


@sentencias.put("/{sentencia_id}", response_model=OneSentenciaOut)
async def modificar_sentencia(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    sentencia_id: int,
    sentencia_in: SentenciaIn,
):
    """Modificar una sentencia"""
    if current_user.permissions.get("SENTENCIAS", 0) < Permiso.MODIFICAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        sentencia = update_sentencia(database, sentencia_id, Sentencia(**sentencia_in.model_dump()))
    except MyAnyError as error:
        return OneSentenciaOut(success=False, message=str(error))
    respuesta = OneSentenciaOut.model_validate(sentencia)
    respuesta.message = "Sentencia actualizada correctamente"
    return respuesta


@sentencias.delete("/{sentencia_id}", response_model=OneSentenciaOut)
async def borrar_sentencia(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    sentencia_id: int,
):
    """Borrar una sentencia"""
    if current_user.permissions.get("SENTENCIAS", 0) < Permiso.BORRAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        sentencia = delete_sentencia(database, sentencia_id)
    except MyAnyError as error:
        return OneSentenciaOut(success=False, message=str(error))
    respuesta = OneSentenciaOut.model_validate(sentencia)
    respuesta.message = "Sentencia eliminada correctamente"
    return respuesta
