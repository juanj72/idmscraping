from src.database.models import session_manager, Pelicula, Actor


class Crud:
    def __init__(self):
        self.session = session_manager

    def addMovie(self, titulo, anio, calificacion, duracion, metascore, url):
        with self.session as session:
            pelicula = Pelicula(
                titulo=titulo,
                anio=anio,
                calificacion=calificacion,
                duracion=duracion,
                metascore=metascore,
                url=url,
            )
            try:
                session.add(pelicula)
                session.commit()
                return pelicula.to_dict()
            except Exception as e:
                session.rollback()
                return f"Error al agregar la película: {e}"

    def addActor(self, nombre):
        with self.session as session:
            actor = Actor(nombre=nombre)
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
