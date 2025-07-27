import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional


class CustomFormatter(logging.Formatter):

    # Códigos de color ANSI
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record):
        # Agregar color para consola
        if hasattr(record, "color") and record.color:
            color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
            record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"

        return super().format(record)


def setup_logger(
    name: str = "imdb_scraper",
    level: str = "INFO",
    log_file: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Configura logger con archivo rotativo y consola

    Args:
        name: Nombre del logger
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Archivo de log (opcional)
        max_bytes: Tamaño máximo por archivo
        backup_count: Número de archivos de respaldo
    """
    logger = logging.getLogger(name)

    # Evitar duplicar handlers si ya está configurado
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, level.upper()))

    # Formato para archivos (sin colores)
    file_formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Formato para consola (con colores)
    console_formatter = CustomFormatter(
        fmt="%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s",
        datefmt="%H:%M:%S",
    )

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(lambda record: setattr(record, "color", True) or True)
    logger.addHandler(console_handler)

    # Handler para archivo (si se especifica)
    if log_file:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Archivo rotativo
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


# Logger global para todo el proyecto
logger = setup_logger(
    name="imdb_scraper",
    level=os.getenv("LOG_LEVEL", "INFO"),
    log_file="src/logs/scraper.log",
)
