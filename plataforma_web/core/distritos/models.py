"""
Distritos, modelos
"""
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Distrito(Base, UniversalMixin):
    """Distrito"""

    # Nombre de la tabla
    __tablename__ = "distritos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    clave = Column(String(16), nullable=False, unique=True)
    nombre = Column(String(256), unique=True, nullable=False)
    nombre_corto = Column(String(64), nullable=False, default="")
    es_distrito_judicial = Column(Boolean(), nullable=False, default=False)
    es_distrito = Column(Boolean, nullable=False, default=False)
    es_jurisdiccional = Column(Boolean, nullable=False, default=False)

    # Hijos
    autoridades = relationship("Autoridad", back_populates="distrito")
    domicilios = relationship("Domicilio", back_populates="distrito")
    oficinas = relationship("Oficina", back_populates="distrito")
    peritos = relationship("Perito", back_populates="distrito")
    repsvm_agresores = relationship("RepsvmAgresor", back_populates="distrito")

    def __repr__(self):
        """Representación"""
        return f"<Distrito {self.clave}>"
