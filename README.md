# 🎬 IMDb Movie Scraper

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
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
- **Elenco**: Lista completa de actores
- **Enlaces**: URL original de IMDb

## 🚀 **Inicio rápido**



### **Instalación local**

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
ENV=development
LOG_LEVEL=INFO

# Base de datos
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=imdb
DATABASE_USER=root
DATABASE_PASSWORD=tu_password

# Scraping
IP_ROTATION=true
MAX_WORKERS=8
DELAY_BETWEEN_REQUESTS=1.0
MAX_RETRIES=3
```

### **Configuraciones disponibles**

| Variable | Descripción | Valores | Default |
|----------|-------------|---------|---------|
| `LOG_LEVEL` | Nivel de logging | DEBUG, INFO, WARNING, ERROR | INFO |
| `IP_ROTATION` | Usar rotación de proxies | `true`/`false` | `false` |
| `MAX_WORKERS` | Hilos concurrentes | 1-20 | 8 |
| `DELAY_BETWEEN_REQUESTS` | Delay entre requests (seg) | 0.5-5.0 | 1.0 |

## 🏗️ **Arquitectura**

```
src/
├── scraper/
│   ├── strategies/          # Estrategias de scraping
│   │   └── bfsp_request.py  # Implementación principal
│   ├── dowloader.py         # Gestión de descargas HTTP
│   ├── proxys/              # Manejo de proxies
│   └── parser.py            # Parseo de JSON-LD
├── database/
│   ├── models.py            # Modelos SQLAlchemy
│   ├── crud.py              # Operaciones CRUD
│   └── session.py           # Gestión de sesiones
├── orchestrator.py          # Coordinador principal
├── config.py                # Configuración del sistema
└── utils/
    └── logger.py            # Sistema de logging
```

### **Patrones implementados**

- **Strategy Pattern**: Diferentes estrategias de scraping
- **Repository Pattern**: Abstracción de acceso a datos
- **Dependency Injection**: Inyección de dependencias
- **Factory Pattern**: Creación de objetos configurables

## 📊 **Uso**

### **Scraping básico**

```python
from src.orchestrator import BfspRequestScraper
from src.scraper.strategies.bfsp_request import BfspRequestScraper as Scraper
from src.scraper.dowloader import DownloaderHelper
from src.database.crud import Crud
from src.config import Config

# Configurar componentes
config = Config()
crud = Crud()
downloader = DownloaderHelper(config)
scraper = Scraper(downloader)

# Crear orchestrator
orchestrator = BfspRequestScraper(scraper, crud, max_workers=8, delay=1.0)

# Ejecutar scraping
url = "https://www.imdb.com/chart/top/?groups=top_250&count=250"
movies = orchestrator.get_movies(url)

print(f"✅ {len(movies)} películas extraídas")
```

### **Consultas a la base de datos**

```python
from src.database.crud import Crud

crud = Crud()

# Obtener todas las películas con actores
movies = crud.get_all_movies_with_actors()

# Top 10 películas mejor calificadas
top_movies = crud.get_top_rated_movies(limit=10)

# Buscar películas por actor
actor_movies = crud.get_movies_by_actor("Leonardo DiCaprio")

# Estadísticas generales
stats = crud.get_movie_stats()
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

**Juan** - [GitHub](https://github.com/tu-usuario)

## 🙏 **Agradecimientos**

- IMDb por proporcionar los datos
- Comunidad de Python por las librerías


---

