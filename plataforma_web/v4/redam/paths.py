"""
REDAM (Registro Estatal de Deudores Alimentarios Morosos) v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_redam, get_redams
from .schemas import OneRedamOut, RedamOut

redam = APIRouter(prefix="/v4/redam", tags=["redam"])


@redam.get("", response_model=CustomPage[RedamOut])
async def paginado_redams(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    autoridad_id: int = None,
    autoridad_clave: str = None,
    distrito_id: int = None,
    distrito_clave: str = None,
    nombre: str = None,
    expediente: str = None,
):
    """Paginado de Deudores Alimentarios Morosos"""
    if current_user.permissions.get("REDAMS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_redams(
            database=database,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            nombre=nombre,
            expediente=expediente,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@redam.get("/{redam_id}", response_model=OneRedamOut)
async def detalle_redam(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    redam_id: int,
):
    """Detalle de un Deudor Alimentario Moroso a partir de su id"""
    if current_user.permissions.get("REDAMS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        deudor = get_redam(database, redam_id)
    except MyAnyError as error:
        return OneRedamOut(success=False, message=str(error))
    return OneRedamOut.model_validate(deudor)
