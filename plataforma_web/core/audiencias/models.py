"""
Audiencias, modelos
"""
from collections import OrderedDict

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Audiencia(Base, UniversalMixin):
    """Audiencia"""

    CARACTERES = OrderedDict(
        [
            ("NO DEFINIDO", "No definido"),
            ("PUBLICA", "Pública"),
            ("PRIVADA", "Privada"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "audiencias"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    autoridad_id = Column(Integer, ForeignKey("autoridades.id"), index=True, nullable=False)
    autoridad = relationship("Autoridad", back_populates="audiencias")

    # Columnas comunes
    tiempo = Column(DateTime, nullable=False)
    tipo_audiencia = Column(String(256), nullable=False)

    # Columnas para Materias C F M L D(CyF) Salas (CyF) TCyA
    expediente = Column(String(64))
    actores = Column(String(256))
    demandados = Column(String(256))

    # Columnas para Materia Acusatorio Penal Oral
    sala = Column(String(256))
    caracter = Column(
        Enum(*CARACTERES, name="tipos_caracteres", native_enum=False),
        index=True,
        nullable=True,
    )
    causa_penal = Column(String(256))
    delitos = Column(String(256))

    # Columnas para Distritales Penales
    toca = Column(String(256))
    expediente_origen = Column(String(256))
    imputados = Column(String(256))

    # Columnas para Salas Penales
    # toca
    # expediente_origen
    # delitos
    origen = Column(String(256))

    @property
    def distrito_id(self):
        """Distrito ID"""
        return self.autoridad.distrito_id

    @property
    def distrito_clave(self):
        """Distrito clave"""
        return self.autoridad.distrito.clave

    @property
    def distrito_nombre(self):
        """Distrito nombre"""
        return self.autoridad.distrito.nombre

    @property
    def distrito_nombre_corto(self):
        """Distrito nombre corto"""
        return self.autoridad.distrito.nombre_corto

    @property
    def autoridad_clave(self):
        """Autoridad clave"""
        return self.autoridad.clave

    @property
    def autoridad_descripcion(self):
        """Autoridad descripción"""
        return self.autoridad.descripcion

    @property
    def autoridad_descripcion_corta(self):
        """Autoridad descripción corta"""
        return self.autoridad.descripcion_corta

    def __repr__(self):
        """Representación"""
        return f"<Audiencia {self.id}>"
