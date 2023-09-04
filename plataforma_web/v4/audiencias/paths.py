"""
Audiencias v4, rutas (paths)
"""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_audiencia, get_audiencias
from .schemas import AudienciaOut, OneAudienciaOut

audiencias = APIRouter(prefix="/v4/audiencias", tags=["audiencias"])


@audiencias.get("", response_model=CustomPage[AudienciaOut])
async def paginado_audiencias(
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
):
    """Paginado de audiencias"""
    if current_user.permissions.get("AUDIENCIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_audiencias(
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
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@audiencias.get("/{audiencia_id}", response_model=OneAudienciaOut)
async def detalle_audiencia(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    audiencia_id: int,
):
    """Detalle de una audiencia a partir de su id"""
    if current_user.permissions.get("AUDIENCIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        audiencia = get_audiencia(database, audiencia_id)
    except MyAnyError as error:
        return OneAudienciaOut(success=False, message=str(error))
    return OneAudienciaOut.model_validate(audiencia)
