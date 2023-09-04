"""
Peritos - Tipos, modelos
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class PeritoTipo(Base, UniversalMixin):
    """PeritoTipo"""

    # Nombre de la tabla
    __tablename__ = "peritos_tipos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombre = Column(String(256), unique=True, nullable=False)

    # Hijos
    peritos = relationship("Perito", back_populates="perito_tipo")

    def __repr__(self):
        """Representación"""
        return f"<PeritoTipo {self.nombre}>"
