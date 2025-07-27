# 🎬 IMDb Movie Scraper

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-green.svg)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Un scraper robusto y escalable para extraer información de películas de IMDb con soporte para proxies, base de datos MySQL y procesamiento concurrente.

## Requisitos:

    python 3.12.8
    poetry 1.7.1

## 🌟 **Características**

- ✅ **Scraping inteligente**: Extracción de datos de IMDb Top 250
- 🎭 **Datos completos**: Películas con actores, ratings y metascores
- 🔄 **Procesamiento concurrente**: Threading optimizado para mejor rendimiento
- 🌐 **Soporte de proxies**: Rotación automática de IPs con fallback
- 🗃️ **Base de datos**: Almacenamiento persistente en MySQL
- 📊 **Logging avanzado**: Sistema de logs con niveles y colores
- 🔒 **VPN Support**: Integración con VPNs gratuitas

## 📋 **Datos extraídos**

Para cada película se obtiene:

- **Información básica**: Título, año, duración
- **Calificaciones**: Rating IMDb y Metascore
- **Elenco**: Lista 3 de actores
- **Enlaces**: URL original de IMDb

## 🚀 **Inicio rápido**

### **Instalación local**

**si quieres ejecutar el proyecto en local, la recomendacion es usar una vpn como **riseupvpn\*\*

```bash
# 1. Crear entorno virtual
poetry shell # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Instalar dependencias
poetry install

# 3. Configurar base de datos MySQL
# Crear database 'imdb' en MySQL

# 4. Ejecutar
python main.py
```

## ⚙️ **Configuración**

### **Archivo .env**

```properties
# Entorno
ENV="development"

# Base de datos
DATABASE_HOST="localhost"
DATABASE_PORT="3306"
DATABASE_NAME="imdb"
DATABASE_USER="root"
DATABASE_PASSWORD="tu_password"

# Scraping
IP_ROTATION=1
```

### **Configuraciones disponibles**

| Variable                 | Descripción                | Valores                     | Default |
| ------------------------ | -------------------------- | --------------------------- | ------- |
| `LOG_LEVEL`              | Nivel de logging           | DEBUG, INFO, WARNING, ERROR | INFO    |
| `IP_ROTATION`            | Usar rotación de proxies   | `true`/`false`              | `false` |
| `MAX_WORKERS`            | Hilos concurrentes         | 1-20                        | 8       |
| `DELAY_BETWEEN_REQUESTS` | Delay entre requests (seg) | 0.5-5.0                     | 1.0     |

## 🏗️ **Arquitectura**

```
idmscraping/
├── main.py                      # 🚀 Punto de entrada principal
├── docker-compose.yml           # 🐳 Configuración Docker
├── pyproject.toml              # 📦 Gestión de dependencias (Poetry)
│
├── src/                        # 📁 Código fuente principal
│   ├── config.py               # ⚙️ Configuración del sistema
│   ├── orchestrator.py         # 🎭 Coordinador principal
│   │
│   ├── scraper/                # 🕷️ Módulo de web scraping
│   │   ├── strategies/         # 📋 Estrategias de scraping
│   │   │   └── bfsp_request.py # 🎯 Implementación principal
│   │   ├── dowloader.py        # 📥 Gestión de descargas HTTP
│   │   ├── parser.py           # 🔍 Parseo de JSON-LD
│   │   └── proxys/             # 🌐 Manejo de proxies
│   │
│   ├── database/               # 🗃️ Módulo de base de datos
│   │   ├── models.py           # 📊 Modelos SQLAlchemy
│   │   ├── crud.py             # 🔄 Operaciones CRUD
│   │   ├── session.py          # 🔗 Gestión de sesiones
│   │   ├── imdb.sql            # 📋 Esquema de BD
│   │   └── queries/            # 📈 Consultas SQL avanzadas
│   │
│   ├── entities/               # 🎬 Entidades de dominio
│   │   └── movies.py           # 🎭 Entidad película
│   │
│   ├── exporter/               # 📤 Exportación de datos
│   │   └── exporter.py         # 💾 Múltiples formatos
│   │
│   ├── tests/                  # 🧪 Suite de tests
│   │   ├── conftest.py         # ⚙️ Configuración pytest
│   │   └── scraper/            # 🕷️ Tests de scraping
│   │
│   └── utils/                  # 🛠️ Utilidades generales
│       └── logger.py           # 📋 Sistema de logging
│
├── data/                       # 📂 Datos y ejemplos
│   ├── html/                   # 🌐 Archivos HTML de prueba
│   └── json_examples/          # 📄 Ejemplos JSON-LD
```

### **Patrones implementados**

- **Strategy Pattern**: Diferentes estrategias de scraping
- **Repository Pattern**: Abstracción de acceso a datos
- **Dependency Injection**: Inyección de dependencias
- **Factory Pattern**: Creación de objetos configurables

## 📊 **Uso**

### \*\* Importacion base de datos

-Tener en cuenta el cargue de la base de datos de acuerdo al .sql, crear una base de datos llamada **imdb** y ejecuta lo siguiente dentro del proyecto
    mysql -u [USUARIO] -p -h [HOST_BASE_DE_DATOS] -P [PUERTO] imdb < src/database/imdb.sql

### **Docker**

-Ejecutar docker compose
docker-compose up -d

### **Scraping básico**

```python
import json
from src.scraper.strategies.bfsp_request import BfspRequestScraper
from src.scraper.dowloader import DownloaderHelper
from src.orchestrator import BfspRequestScraper as OrchestratorBfspRequestScraper
import time
from src.database.crud import Crud
from src.scraper.proxys.get_proxys import fetch_proxies
from src.config import Config
from src.utils.logger import logger
from src.exporter.exporter import export_to_csv

if __name__ == "__main__":

    start_time = time.time()
    logger.info("Iniciando el scraper de películas de IMDB...")
    config = Config()
    logger.info(f"Configuración cargada ..")
    fetch_proxies("https")  # Uncomment to fetch proxies and cache them
    logger.info("Proxies cacheados correctamente.")
    logger.info("Iniciando el downloader helper...")
    crud = Crud()
    downloader = DownloaderHelper(config)
    url = "https://www.imdb.com/chart/top/?groups=top_250&count=250"
    scraper = BfspRequestScraper(downloader)

    orchestrator_scraper = OrchestratorBfspRequestScraper(scraper, crud, 12, 0)
    movies = orchestrator_scraper.get_movies(url)
    logger.info(f"Películas obtenidas: {len(movies)}")
    # Export to CSV
    export_to_csv(movies, "movies")

    end_time = time.time()
    logger.info(f"Tiempo total de ejecución: {end_time - start_time:.2f} segundos")

```

### **Servicios incluidos**

- **db**: Base de datos MySQL 8.0

## 📈 **Performance**

### **Benchmarks típicos**

- **250 películas**: ~45-60 segundos
- **Memoria usage**: ~150-200MB
- **CPU usage**: Moderate (depende de MAX_WORKERS)
- **Requests/segundo**: ~8-12 (con rate limiting)

### **Optimizaciones implementadas**

- ✅ Conexiones HTTP reutilizables
- ✅ Threading pool optimizado
- ✅ Batch inserts en base de datos
- ✅ Caching de proxies
- ✅ Lazy loading de relaciones

## 🔧 **Desarrollo**

### **Linting y formato**

```bash

# Linting
flake8 src/

# Type checking
mypy src/
```

### **Agregar nueva estrategia de scraping**

```python
# src/scraper/strategies/nueva_estrategia.py
from src.scraper.base import BaseScraper

class NuevaEstrategia(BaseScraper):
    def get_data(self, url: str) -> dict:
        # Implementar lógica específica
        pass
```

## 🐛 **Troubleshooting**

### **Problemas comunes**

    variar la env var "IP_ROTATION="1" # 0: False, 1: True" para que cuando al ejecutar el docker se pueda evidenciar la rotacion de ips desde la vpn, y se realice la inserción

## 📊 **Monitoreo**

### **Verificar estado**

```python
# Verificar IP actual (si usas VPN)
curl https://ipinfo.io/json

# Estadísticas de base de datos
python -c "from src.database.crud import Crud; print(Crud().get_movie_stats())"
```

## 🤝 **Contribuir**

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Crear Pull Request

## 📝 **TODO**

- [ ] Agregar soporte para más sitios (Rotten Tomatoes, etc.)
- [ ] Implementar API REST
- [ ] Dashboard web para monitoreo
- [ ] Notificaciones por email/Slack
- [ ] Export a diferentes formatos (CSV, JSON, XML)
- [ ] Scraping incremental (solo películas nuevas)

## 👨‍💻 **Autor**

**Juan** - [GitHub](https://github.com/juanj72)

## 🙏 **Agradecimientos**

- Comunidad de Python por las librerías

---
