"""
Usuarios-Roles v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.usuarios_roles.models import UsuarioRol
from ..roles.crud import get_rol
from ..usuarios.crud import get_usuario, get_usuario_with_email


def get_usuarios_roles(
    database: Session,
    rol_id: int = None,
    rol_nombre: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
) -> Any:
    """Consultar los usuarios-roles activos"""
    consulta = database.query(UsuarioRol)
    if rol_id is not None:
        rol = get_rol(database, rol_id)
        consulta = consulta.filter(rol == rol)
    elif rol_nombre is not None:
        rol = (database, rol_nombre)
        consulta = consulta.filter(rol == rol)
    if usuario_id is not None:
        usuario = get_usuario(database, usuario_id)
        consulta = consulta.filter(usuario == usuario)
    elif usuario_email is not None:
        usuario = get_usuario_with_email(database, usuario_email)
        consulta = consulta.filter(usuario == usuario)
    return consulta.filter_by(estatus="A").order_by(UsuarioRol.id.desc())


def get_usuario_rol(database: Session, usuario_rol_id: int) -> UsuarioRol:
    """Consultar un usuario-rol por su id"""
    usuario_rol = database.query(UsuarioRol).get(usuario_rol_id)
    if usuario_rol is None:
        raise MyNotExistsError("No existe ese usuario-rol")
    if usuario_rol.estatus != "A":
        raise MyIsDeletedError("No es activo ese usuario-rol, está eliminado")
    return usuario_rol
