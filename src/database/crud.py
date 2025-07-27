from src.database.models import session, Pelicula, Actor
from src.entities.movies import Movie, Actor as EntityActor
from sqlalchemy.orm import joinedload
from typing import List, Dict, Any
from src.utils.logger import logger


class Crud:
    def __init__(self):
        self.session = session

    def addMovie(self, movie: Movie) -> dict | str:
        with self.session.session_scope() as session:
            pelicula = Pelicula(
                titulo=movie.title,
                anio=movie.year,
                calificacion=movie.qualification,
                duracion=movie.duration,
                metascore=movie.metascore,
                url=movie.url,
            )
            try:
                session.add(pelicula)
                session.commit()
                return pelicula.to_dict()
            except Exception as e:
                session.rollback()
                return f"Error al agregar la película: {e}"

    def addActor(self, actor: EntityActor) -> dict | str:
        with self.session.session_scope() as session:
            actor = Actor(nombre=actor.name)
            try:
                session.add(actor)
                session.commit()
                return actor.to_dict()
            except Exception as e:
                session.rollback()
                return f"Error al agregar el actor: {e}"

    def addActorToMovie(self, pelicula_id, actor_id):
        with self.session.session_scope() as session:
            try:
                pelicula = session.query(Pelicula).filter_by(id=pelicula_id).one()
                actor = session.query(Actor).filter_by(id=actor_id).one()
                pelicula.actores.append(actor)
                session.commit()
                return f"Actor {actor.nombre} agregado a la película {pelicula.titulo}"
            except Exception as e:
                session.rollback()
                return f"Error al agregar el actor a la película: {e}"

    def getMovie(self, pelicula_id):
        with self.session.session_scope() as session:
            try:
                pelicula = session.query(Pelicula).filter_by(id=pelicula_id).one()
                return pelicula.to_dict()
            except Exception as e:
                return f"Error al obtener la película: {e}"

    def getMovieByUrl(self, url):
        with self.session.session_scope() as session:
            try:
                pelicula = session.query(Pelicula).filter_by(url=url).one()
                return pelicula.to_dict()
            except Exception as e:
                return f"Error al obtener la película por URL: {e}"

    def getActor(self, actor_name):
        with self.session.session_scope() as session:
            try:
                actor = session.query(Actor).filter_by(nombre=actor_name).one_or_none()
                if actor:
                    return actor.to_dict()
                else:
                    return None
            except Exception as e:
                return f"Error al obtener el actor: {e}"

    def getMovieActor(self, pelicula_id, actor_id):
        with self.session.session_scope() as session:
            try:
                pelicula = session.query(Pelicula).filter_by(id=pelicula_id).one()
                actor = session.query(Actor).filter_by(id=actor_id).one()
                return {"pelicula": pelicula.to_dict(), "actor": actor.to_dict()}
            except Exception as e:
                return f"Error al obtener la película o el actor: {e}"

    def get_all_movies_with_actors(self) -> List[Dict[str, Any]]:
        
        logger.info("🎬 Obteniendo todas las películas con actores...")

        with self.session.session_scope() as session:
            try:
                peliculas = (
                    session.query(Pelicula).options(joinedload(Pelicula.actores)).all()
                )

                result = [pelicula.to_dict() for pelicula in peliculas]

                logger.info(f"✅ {len(result)} películas obtenidas con sus actores")
                return result

            except Exception as e:
                logger.error(f"❌ Error obteniendo películas: {e}")
                raise
