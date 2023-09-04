"""
REPSVM Agresores v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_repsvm_agresor, get_repsvm_agresores
from .schemas import OneRepsvmAgresorOut, RepsvmAgresorOut

repsvm_agresores = APIRouter(prefix="/v4/repsvm_agresores", tags=["repsvm agresores"])


@repsvm_agresores.get("", response_model=CustomPage[RepsvmAgresorOut])
async def paginado_repsvm_agresores(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    distrito_id: int = None,
    distrito_clave: str = None,
    nombre: str = None,
):
    """Paginado de agresores"""
    if current_user.permissions.get("REPSVM AGRESORES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_repsvm_agresores(
            database=database,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            nombre=nombre,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@repsvm_agresores.get("/{repsvm_agresor_id}", response_model=OneRepsvmAgresorOut)
async def detalle_repsvm_agresor(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    repsvm_agresor_id: int,
):
    """Detalle de una agresor a partir de su id"""
    if current_user.permissions.get("REPSVM AGRESORES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        repsvm_agresor = get_repsvm_agresor(database, repsvm_agresor_id)
    except MyAnyError as error:
        return OneRepsvmAgresorOut(success=False, message=str(error))
    return OneRepsvmAgresorOut.model_validate(repsvm_agresor)
