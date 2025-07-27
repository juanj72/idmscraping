import pandas as pd
from src.utils.logger import logger


def export_to_csv(data: dict, name: str = "movies_export"):
    """
    Exporta los datos a un archivo CSV.
    """
    try:
        df = pd.DataFrame(data)
        df.to_csv(f"src/data/{name}.csv", index=False)
        logger.info(f"Datos exportados exitosamente a src/data/{name}.csv")
    except Exception as e:
        logger.error(f"Error al exportar los datos: {e}")
