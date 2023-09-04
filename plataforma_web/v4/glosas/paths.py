"""
Glosas v4, rutas (paths)
"""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.glosas.models import Glosa
from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import create_glosa, delete_glosa, elaborate_daily_report_glosas, get_glosa, get_glosas, update_glosa
from .schemas import GlosaIn, GlosaOut, OneGlosaOut

glosas = APIRouter(prefix="/v4/glosas", tags=["glosas"])


@glosas.get("", response_model=CustomPage[GlosaOut])
async def paginado_glosas(
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
    expediente: str = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
):
    """Paginado de glosas"""
    if current_user.permissions.get("GLOSAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_glosas(
            database=database,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            expediente=expediente,
            anio=anio,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@glosas.get("/reporte_diario", response_model=CustomList[GlosaOut])
async def reporte_diario_glosas(
    creado: date,
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Reporte diario de glosas"""
    if current_user.permissions.get("GLOSAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = elaborate_daily_report_glosas(database, creado)
    except MyAnyError as error:
        return CustomList(success=False, message=str(error))
    if not resultados:
        return CustomList(success=True, message="No hay glosas creadas en la fecha indicada", total=0)
    return CustomList(
        success=True,
        message="Sucess",
        total=len(resultados),
        items=resultados,
        page=1,
        size=len(resultados),
        pages=1,
    )


@glosas.get("/{glosa_id}", response_model=OneGlosaOut)
async def detalle_glosa(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    glosa_id: int,
):
    """Detalle de una glosa a partir de su id"""
    if current_user.permissions.get("GLOSAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        glosa = get_glosa(database, glosa_id)
    except MyAnyError as error:
        return OneGlosaOut(success=False, message=str(error))
    return OneGlosaOut.model_validate(glosa)


@glosas.post("", response_model=OneGlosaOut)
async def crear_glosa(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    glosa_in: GlosaIn,
):
    """Crear una glosa"""
    if current_user.permissions.get("GLOSAS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        glosa = create_glosa(database, Glosa(**glosa_in.model_dump()))
    except MyAnyError as error:
        return OneGlosaOut(success=False, message=str(error))
    respuesta = OneGlosaOut.model_validate(glosa)
    respuesta.message = "Glosa creada correctamente"
    return respuesta


@glosas.put("/{glosa_id}", response_model=OneGlosaOut)
async def modificar_glosa(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    glosa_id: int,
    glosa_in: GlosaIn,
):
    """Modificar una glosa"""
    if current_user.permissions.get("GLOSAS", 0) < Permiso.MODIFICAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        glosa = update_glosa(database, glosa_id, Glosa(**glosa_in.model_dump()))
    except MyAnyError as error:
        return OneGlosaOut(success=False, message=str(error))
    respuesta = OneGlosaOut.model_validate(glosa)
    respuesta.message = "Glosa actualizada correctamente"
    return respuesta


@glosas.delete("/{glosa_id}", response_model=OneGlosaOut)
async def borrar_glosa(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    glosa_id: int,
):
    """Borrar una glosa"""
    if current_user.permissions.get("GLOSAS", 0) < Permiso.BORRAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        glosa = delete_glosa(database, glosa_id)
    except MyAnyError as error:
        return OneGlosaOut(success=False, message=str(error))
    respuesta = OneGlosaOut.model_validate(glosa)
    respuesta.message = "Glosa borrada correctamente"
    return respuesta
