"""
Materias, modelos
"""
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Materia(Base, UniversalMixin):
    """Materia"""

    # Nombre de la tabla
    __tablename__ = "materias"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    clave = Column(String(16), nullable=False, unique=True)
    nombre = Column(String(64), unique=True, nullable=False)
    en_sentencias = Column(Boolean, nullable=False, default=False)

    # Hijos
    autoridades = relationship("Autoridad", back_populates="materia")
    materias_tipos_juicios = relationship("MateriaTipoJuicio", back_populates="materia")

    def __repr__(self):
        """Representación"""
        return f"<Materia {self.nombre}>"
