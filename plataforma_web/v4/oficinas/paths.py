"""
Oficinas v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_oficina_with_clave, get_oficinas
from .schemas import OficinaListOut, OficinaOut, OneOficinaOut

oficinas = APIRouter(prefix="/v4/oficinas", tags=["oficinas"])


@oficinas.get("", response_model=CustomPage[OficinaOut])
async def paginado_oficinas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    distrito_id: int = None,
    distrito_clave: str = None,
    domicilio_id: int = None,
    es_jurisdiccional: bool = None,
):
    """Paginado de oficinas"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_oficinas(
            database=database,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            domicilio_id=domicilio_id,
            es_jurisdiccional=es_jurisdiccional,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@oficinas.get("/listado", response_model=CustomList[OficinaListOut])
async def listado_oficinas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    distrito_id: int = None,
    distrito_clave: str = None,
    domicilio_id: int = None,
    es_jurisdiccional: bool = None,
):
    """Listado de oficinas"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_oficinas(
            database=database,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            domicilio_id=domicilio_id,
            es_jurisdiccional=es_jurisdiccional,
        )
    except MyAnyError as error:
        return CustomList(success=False, message=str(error))
    return paginate(resultados)


@oficinas.get("/{oficina_clave}", response_model=OneOficinaOut)
async def detalle_oficina(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    oficina_clave: str,
):
    """Detalle de una oficina a partir de su clave"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        oficina = get_oficina_with_clave(database, oficina_clave)
    except MyAnyError as error:
        return OneOficinaOut(success=False, message=str(error))
    return OneOficinaOut.model_validate(oficina)
