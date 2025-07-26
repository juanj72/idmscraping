from src.database.models import session_manager, Pelicula, Actor
from src.entities.movies import Movie, Actor as EntityActor


class Crud:
    def __init__(self):
        self.session = session_manager

    def addMovie(self, movie: Movie) -> dict:
        with self.session as session:
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

    def addActor(self, actor: EntityActor) -> dict:
        with self.session as session:
            actor = Actor(nombre=actor.name)
            try:
                session.add(actor)
                session.commit()
                return actor.to_dict()
            except Exception as e:
                session.rollback()
                return f"Error al agregar el actor: {e}"

    def addActorToMovie(self, pelicula_id, actor_id):
        with self.session as session:
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
        with self.session as session:
            try:
                pelicula = session.query(Pelicula).filter_by(id=pelicula_id).one()
                return pelicula.to_dict()
            except Exception as e:
                return f"Error al obtener la película: {e}"

    def getMovieByUrl(self, url):
        with self.session as session:
            try:
                pelicula = session.query(Pelicula).filter_by(url=url).one()
                return pelicula.to_dict()
            except Exception as e:
                return f"Error al obtener la película por URL: {e}"

    def getActor(self, actor_id):
        with self.session as session:
            try:
                actor = session.query(Actor).filter_by(id=actor_id).one()
                return actor.to_dict()
            except Exception as e:
                return f"Error al obtener el actor: {e}"

    def getMovieActor(self, pelicula_id, actor_id):
        with self.session as session:
            try:
                pelicula = session.query(Pelicula).filter_by(id=pelicula_id).one()
                actor = session.query(Actor).filter_by(id=actor_id).one()
                return {"pelicula": pelicula.to_dict(), "actor": actor.to_dict()}
            except Exception as e:
                return f"Error al obtener la película o el actor: {e}"
