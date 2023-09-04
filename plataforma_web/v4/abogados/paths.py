"""
Abogados v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_abogado, get_abogados
from .schemas import AbogadoOut, OneAbogadoOut

abogados = APIRouter(prefix="/v4/abogados", tags=["abogados"])


@abogados.get("", response_model=CustomPage[AbogadoOut])
async def paginado_abogados(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    nombre: str = None,
    anio_desde: int = None,
    anio_hasta: int = None,
):
    """Paginado de abogados"""
    if current_user.permissions.get("ABOGADOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_abogados(
            database=database,
            nombre=nombre,
            anio_desde=anio_desde,
            anio_hasta=anio_hasta,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@abogados.get("/{abogado_id}", response_model=OneAbogadoOut)
async def detalle_abogado(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    abogado_id: int,
):
    """Detalle de un abogado a partir de su id"""
    if current_user.permissions.get("ABOGADOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        abogado = get_abogado(database, abogado_id)
    except MyAnyError as error:
        return OneAbogadoOut(success=False, message=str(error))
    return OneAbogadoOut.model_validate(abogado)
