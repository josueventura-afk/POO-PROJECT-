from datetime import date

from sqlalchemy import Column, String, Date, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from models.estudiante import Estudiante
from models.control_salud import ControlSalud
from models.medida import Peso, Talla
from .database import Base, SessionLocal, engine


class EstudianteDB(Base):
    __tablename__ = "estudiantes"

    codigo = Column(String(50), primary_key=True)
    nombre_completo = Column(String(200), nullable=False)
    fecha_nacimiento = Column(String(10), nullable=False)
    sexo = Column(String(1), nullable=False)
    curso = Column(String(100), nullable=False)
    controles = relationship("ControlSaludDB", back_populates="estudiante", cascade="all, delete-orphan")


class ControlSaludDB(Base):
    __tablename__ = "controles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    estudiante_codigo = Column(String(50), ForeignKey("estudiantes.codigo"), nullable=False)
    fecha = Column(Date, nullable=False)
    peso = Column(Float, nullable=False)
    talla = Column(Float, nullable=False)
    observaciones = Column(String(500), nullable=True)
    estudiante = relationship("EstudianteDB", back_populates="controles")


class EstudianteRepository:
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory
        self.crear_tablas()

    def crear_tablas(self):
        Base.metadata.create_all(engine)

    def guardar_estudiante(self, estudiante: Estudiante):
        with self.session_factory() as session:
            db_estudiante = EstudianteDB(
                codigo=estudiante.codigo,
                nombre_completo=estudiante.nombre_completo,
                fecha_nacimiento=estudiante.fecha_nacimiento,
                sexo=estudiante.sexo,
                curso=estudiante.curso,
            )
            session.add(db_estudiante)
            session.commit()

    def guardar_control(self, estudiante_codigo: str, control: ControlSalud):
        with self.session_factory() as session:
            db_estudiante = session.get(EstudianteDB, estudiante_codigo)
            if not db_estudiante:
                raise ValueError("Estudiante no encontrado para registrar control")

            db_control = ControlSaludDB(
                estudiante_codigo=estudiante_codigo,
                fecha=control.fecha,
                peso=control.peso.get_valor(),
                talla=control.talla.get_valor(),
                observaciones=control.observaciones,
            )
            session.add(db_control)
            session.commit()

    def cargar_estudiantes(self):
        with self.session_factory() as session:
            estudiantes = []
            db_estudiantes = session.query(EstudianteDB).all()
            for db_est in db_estudiantes:
                estudiante = Estudiante(
                    db_est.codigo,
                    db_est.nombre_completo,
                    db_est.fecha_nacimiento,
                    db_est.sexo,
                    db_est.curso,
                )
                controles_ordenados = sorted(db_est.controles, key=lambda c: c.fecha)
                for db_control in controles_ordenados:
                    control = ControlSalud(
                        db_control.fecha,
                        Peso(db_control.peso),
                        Talla(db_control.talla),
                        db_control.observaciones or "",
                    )
                    estudiante.agregar_control(control)
                estudiantes.append(estudiante)
            return estudiantes

    def buscar_estudiante(self, codigo: str):
        with self.session_factory() as session:
            return session.get(EstudianteDB, codigo)

    def actualizar_estudiante(self, codigo: str, **kwargs):
        with self.session_factory() as session:
            db_est = session.get(EstudianteDB, codigo)
            if not db_est:
                raise ValueError("Estudiante no encontrado")
            for clave, valor in kwargs.items():
                if hasattr(db_est, clave):
                    setattr(db_est, clave, valor)
            session.commit()

    def eliminar_estudiante(self, codigo: str):
        with self.session_factory() as session:
            db_est = session.get(EstudianteDB, codigo)
            if not db_est:
                raise ValueError("Estudiante no encontrado")
            session.delete(db_est)
            session.commit()
