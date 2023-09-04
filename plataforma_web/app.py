"""
PJECZ Plataforma Web API Key
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from config.settings import get_settings

from .v4.abogados.paths import abogados
from .v4.audiencias.paths import audiencias
from .v4.autoridades.paths import autoridades
from .v4.distritos.paths import distritos
from .v4.domicilios.paths import domicilios
from .v4.edictos.paths import edictos
from .v4.glosas.paths import glosas
from .v4.listas_de_acuerdos.paths import listas_de_acuerdos
from .v4.materias.paths import materias
from .v4.materias_tipos_juicios.paths import materias_tipos_juicios
from .v4.modulos.paths import modulos
from .v4.oficinas.paths import oficinas
from .v4.peritos.paths import peritos
from .v4.peritos_tipos.paths import peritos_tipos
from .v4.permisos.paths import permisos
from .v4.redam.paths import redam
from .v4.repsvm_agresores.paths import repsvm_agresores
from .v4.roles.paths import roles
from .v4.sentencias.paths import sentencias
from .v4.ubicaciones_expedientes.paths import ubicaciones_expedientes
from .v4.usuarios.paths import usuarios
from .v4.usuarios_roles.paths import usuarios_roles


def create_app() -> FastAPI:
    """Crea la aplicación FastAPI"""

    # FastAPI
    app = FastAPI(
        title="PJECZ Plataforma Web API Key",
        description="API del Poder Judicial del Estado de Coahuila de Zaragoza. Hecho con FastAPI.",
        docs_url="/docs",
        redoc_url=None,
    )

    # CORSMiddleware
    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins.split(","),
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    # Rutas
    app.include_router(abogados)
    app.include_router(audiencias)
    app.include_router(autoridades)
    app.include_router(distritos)
    app.include_router(domicilios)
    app.include_router(edictos)
    app.include_router(glosas)
    app.include_router(listas_de_acuerdos)
    app.include_router(materias)
    app.include_router(materias_tipos_juicios)
    app.include_router(modulos)
    app.include_router(oficinas)
    app.include_router(peritos)
    app.include_router(peritos_tipos)
    app.include_router(permisos)
    app.include_router(redam)
    app.include_router(repsvm_agresores)
    app.include_router(roles)
    app.include_router(sentencias)
    app.include_router(ubicaciones_expedientes)
    app.include_router(usuarios)
    app.include_router(usuarios_roles)

    # Paginación
    add_pagination(app)

    # Mensaje de Bienvenida
    @app.get("/")
    async def root():
        """Mensaje de Bienvenida"""
        return {"message": "API del Poder Judicial del Estado de Coahuila de Zaragoza. Hecho con FastAPI."}

    # Entregar
    return app
