from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.database.session import SessionManager
from src.config import Config

config = Config()
session = SessionManager(config)
session_manager = session.get_session()
Base = session.base


peliculas_actores = Table(
    "peliculas_actores",
    Base.metadata,
    Column(
        "pelicula_id",
        Integer,
        ForeignKey("peliculas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "actor_id",
        Integer,
        ForeignKey("actores.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Pelicula(Base):
    __tablename__ = "peliculas"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(255), nullable=False)
    anio = Column(Integer, nullable=False)
    calificacion = Column(Integer)
    duracion = Column(Float)
    metascore = Column(Float)
    url = Column(String(512), nullable=False, unique=True)

    actores = relationship(
        "Actor", secondary=peliculas_actores, back_populates="peliculas"
    )


class Actor(Base):
    __tablename__ = "actores"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), nullable=False, unique=True)

    peliculas = relationship(
        "Pelicula", secondary=peliculas_actores, back_populates="actores"
    )
