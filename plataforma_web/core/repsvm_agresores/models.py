"""
REPSVM Agresores, modelos
"""
from collections import OrderedDict

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class RepsvmAgresor(Base, UniversalMixin):
    """RepsvmAgresor"""

    TIPOS_JUZGADOS = OrderedDict(
        [
            ("ND", "No Definido"),
            ("JUZGADO ESPECIALIZADO EN VIOLENCIA CONTRA LAS MUJERES", "Juzgado Especializado en Violencia contra las Mujeres"),
            ("JUZGADO ESPECIALIZADO EN VIOLENCIA FAMILIAR", "Juzgado Especializado en Violencia Familiar"),
            ("JUZGADO DE PRIMERA INSTANCIA EN MATERIA PENAL", "Juzgado de Primera Instancia en Materia Penal"),
        ]
    )

    TIPOS_SENTENCIAS = OrderedDict(
        [
            ("ND", "No Definido"),
            ("PROCEDIMIENTO ABREVIADO", "Procedimiento Abreviado"),
            ("JUICIO ORAL", "Juicio Oral"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "repsvm_agresores"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    distrito_id = Column(Integer, ForeignKey("distritos.id"), index=True, nullable=False)
    distrito = relationship("Distrito", back_populates="repsvm_agresores")

    # Columnas
    consecutivo = Column(Integer(), nullable=False)
    delito_generico = Column(String(256), nullable=False)
    delito_especifico = Column(String(1024), nullable=False)
    es_publico = Column(Boolean(), default=False, nullable=False)
    nombre = Column(String(256), nullable=False)
    numero_causa = Column(String(256), nullable=False)
    pena_impuesta = Column(String(256), nullable=False)
    observaciones = Column(Text(), nullable=True)
    sentencia_url = Column(String(512), nullable=True)
    tipo_juzgado = Column(Enum(*TIPOS_JUZGADOS, name="tipos_juzgados", native_enum=False), index=True, nullable=False)
    tipo_sentencia = Column(Enum(*TIPOS_SENTENCIAS, name="tipos_juzgados", native_enum=False), index=True, nullable=False)

    @property
    def distrito_clave(self):
        """Distrito clave"""
        return self.distrito.clave

    @property
    def distrito_nombre(self):
        """Distrito nombre"""
        return self.distrito.nombre

    @property
    def distrito_nombre_corto(self):
        """Distrito nombre corto"""
        return self.distrito.nombre_corto

    def __repr__(self):
        """Representación"""
        return f"<RepsvmAgresor {self.id}>"
