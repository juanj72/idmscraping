from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from typing import Generator
from src.config import Config


class SessionManager:
    def __init__(self, config: Config):
        self.config = config.config
        self.database_url = (
            f"mysql+pymysql://{self.config['database']['user']}:{self.config['database']['password']}"
            f"@{self.config['database']['host']}:{self.config['database']['port']}/{self.config['database']['name']}"
        )
        self.engine = create_engine(
            self.database_url,
            echo=False,
            future=True,
        )
        self.SessionLocal = sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False
        )
        self._base = declarative_base()

    def get_session(self):
        return self.SessionLocal()

    @contextmanager
    def session_scope(self) -> Generator:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @property
    def base(self):
        return self._base

    def test_connection(self) -> bool:
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"❌ Fallo en la conexión: {e}")
            return False
