from src.database.models import session_manager, Pelicula

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
                url=url
            )
            session.add(pelicula)
            session.commit()

