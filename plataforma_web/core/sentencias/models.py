"""
Sentencias, modelos
"""
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Sentencia(Base, UniversalMixin):
    """Sentencia"""

    # Nombre de la tabla
    __tablename__ = "sentencias"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    autoridad_id = Column(Integer, ForeignKey("autoridades.id"), index=True, nullable=False)
    autoridad = relationship("Autoridad", back_populates="sentencias")
    materia_tipo_juicio_id = Column(Integer, ForeignKey("materias_tipos_juicios.id"), index=True, nullable=False)
    materia_tipo_juicio = relationship("MateriaTipoJuicio", back_populates="sentencias")

    # Columnas
    sentencia = Column(String(16), nullable=False)
    sentencia_fecha = Column(Date, index=True, nullable=True)
    expediente = Column(String(16), nullable=False)
    expediente_anio = Column(Integer)
    expediente_num = Column(Integer)
    fecha = Column(Date, index=True, nullable=False)
    descripcion = Column(String(1024), nullable=False)
    es_perspectiva_genero = Column(Boolean, nullable=False, default=False)
    archivo = Column(String(256), nullable=False)
    url = Column(String(512), nullable=False)

    @property
    def descargar_url(self):
        """URL para descargar el archivo desde el sitio web"""
        if self.id:
            return f"https://www.pjecz.gob.mx/consultas/sentencias/descargar/?id={self.id}"
        return ""

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

    @property
    def materia_id(self):
        """Materia ID"""
        return self.materia_tipo_juicio.materia_id

    @property
    def materia_nombre(self):
        """Nombre de la materia"""
        return self.materia_tipo_juicio.materia.nombre

    @property
    def materia_tipo_juicio_descripcion(self):
        """Descripción del tipo de juicio"""
        return self.materia_tipo_juicio.descripcion

    def __repr__(self):
        """Representación"""
        return f"<Sentencia {self.id}>"
