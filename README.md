# Incident Response Plan Health API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0+-blue.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-green.svg)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-1.7+-yellow.svg)](https://alembic.sqlalchemy.org/)

A robust FastAPI-based backend service for managing incident response plans in healthcare settings. The API provides full CRUD operations for an `Incident` resource and is implemented with SQLAlchemy and Pydantic, with support for both SQLite (development) and MySQL (production) databases.

This README documents how to set up, configure, run, and develop the backend. It also documents the available API endpoints, data models, and notes about switching between local SQLite and production MySQL databases.

## 📑 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Local Development Setup (SQLite)](#local-development-setup-sqlite)
  - [Production Setup (MySQL)](#production-setup-mysql)
- [Configuration](#configuration)
- [Database Management](#database-management)
  - [Migrations](#migrations)
  - [Schema Updates](#schema-updates)
- [API Reference](#api-reference)
- [Development](#development)
  - [Testing Tools](#testing-tools)
  - [Development Commands](#development-commands)
- [Security](#security)
- [Contacts](#contacts)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **RESTful API Operations**
  - Full CRUD functionality for incident management
  - Paginated list endpoints
  - Detailed error responses

- **Data Validation & Security**
  - Input validation using Pydantic schemas
  - Type checking and data sanitization
  - Configurable CORS support

- **Database & Storage**
  - SQLAlchemy ORM with async support
  - Multi-database support (SQLite/MySQL)
  - Alembic migrations for schema management

- **Developer Experience**
  - Auto-generated OpenAPI documentation
  - Comprehensive test suite
  - Development automation via Makefile
  - Multiple testing tools (HTTPie, Postman)

## 🛠 Technology Stack

- **Core Framework**
  - Python 3.12+
  - FastAPI 0.68.0+
  - Uvicorn (ASGI server)

- **Database & ORM**
  - SQLAlchemy 2.0+
  - Alembic 1.7+ (migrations)
  - SQLite (development)
  - MySQL (production)

- **Testing & Development**
  - httpx (API testing)
  - HTTPie (CLI testing)
  - Postman (API collection)
  - pytest (unit tests)

## 📁 Project Structure

```
backend/
├── README.md                # Project documentation
├── Makefile                # Development automation
├── requirements.txt        # Python dependencies
├── main.py                # Application entry point
├── init_db.py             # Database initialization
│
├── alembic/               # Database migrations
│   ├── versions/         # Migration scripts
│   ├── env.py           # Migration environment
│   └── alembic.ini      # Migration configuration
│
├── app/                   # Application package
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLAlchemy models
│   ├── routes.py         # API endpoints
│   └── schemas.py        # Pydantic schemas
│
├── tests/                # Test suite
│   └── test_api.py      # API tests
│
├── httpie_examples.sh    # HTTPie test scripts
└── postman_collection.json # Postman API collection
```

## 🚀 Getting Started

### Local Development Setup (SQLite)

1. **Create Python Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Database**
   ```bash
   make migrate  # Runs all migrations
   # or
   alembic upgrade head
   ```

4. **Start Development Server**
   ```bash
   make start
   # or
   python main.py
   ```

5. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Production Setup (MySQL)

1. **Set up MySQL Server**
   - Install MySQL
   - Create database: `incidents_db`

2. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Update MySQL credentials

3. **Initialize Production Database**
   ```bash
   make init-db    # Creates MySQL database
   make migrate    # Applies migrations
   ```

4. **Deploy Application**
   ```bash
   # Using process manager (e.g., supervisord)
   supervisord -c supervisor.conf

   # Or directly with uvicorn
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## ⚙️ Configuration

Create `.env` file in project root:

```env
# Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=incidents_db

# Application Settings
HOST=0.0.0.0
PORT=8000
```

## 💾 Database Management

### Database migrations

The project uses Alembic for database migrations. Migration files are in the `alembic/` directory. Managed with Alembic:
- `alembic/versions/0001_initial.py` - Creates the incidents table
- Future migrations will be added here when you run `make makemigrations`

The migration system uses your SQLAlchemy models from `app/models.py` to detect schema changes.

#### First-time setup

If you have existing tables (created by `Base.metadata.create_all()`), you can start using Alembic without applying the initial migration:

```bash
alembic stamp head  # marks existing tables as migrated
```

Then create new migrations for future schema changes.

#### Running migrations

1. Ensure your database is running and `.env` has correct credentials

2. Apply all migrations:
```bash
make migrate
# or
alembic upgrade head  # applies all pending migrations
```

3. To create a new migration (after changing models):
```bash
make makemigrations
# or
alembic revision --autogenerate -m "describe your changes"
```

4. To roll back one version:
```bash
alembic downgrade -1
```

#### Migration files

- `alembic/versions/0001_initial.py` - Creates the incidents table
- Future migrations will be added here when you run `make makemigrations`

The migration system uses your SQLAlchemy models from `app/models.py` to detect schema changes.

### Schema Updates

Current model schema (`app/models.py`):

```python
class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    description = Column(String(500))
    location = Column(String(100))
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

## 📚 API Reference

### Incidents API

Base URL: `/api/v1`

#### Create Incident
- **POST** `/incidents/`
  ```json
  {
    "incident_type": "Medication Error",
    "description": "Wrong medication dosage administered",
    "location": "Ward A",
    "date_time": "2025-11-08T00:24:54.509Z",
    "severity_level": "high",
    "contact_information": "07011111111"
  }
  ```

#### List Incidents
- **GET** `/incidents/`
  - Query Parameters:
    - `skip` (int, default=0)
    - `limit` (int, default=100)
  - Response: Array of incidents

#### Get Incident
- **GET** `/incidents/{incident_id}`
  - Path Parameters:
    - `incident_id` (int)
  - Response: Single incident object

#### Update Incident
- **PUT** `/incidents/{incident_id}`
  - Path Parameters:
    - `incident_id` (int)
  - Request Body: Updated incident fields
  - Response: Updated incident object

#### Delete Incident
- **DELETE** `/incidents/{incident_id}`
  - Path Parameters:
    - `incident_id` (int)
  - Response: Success message

## 🔧 Development

### Testing Tools

1. **API Tests**
   ```bash
   make test  # Runs test suite
   ```

2. **HTTPie Testing**
   ```bash
   ./httpie_examples.sh
   ```

3. **Postman Collection**
   - Import `postman_collection.json`
   - Contains all endpoint examples

### Development Commands

Available `make` commands:

```bash
make start           # Start FastAPI server
make test           # Run test suite
make migrate        # Apply database migrations
make makemigrations # Create new migration
make init-db        # Initialize MySQL database
```

## 🔐 Security

- Environment variables for sensitive data
- CORS configuration for web security
- Database connection pooling
- Input validation and sanitization
- Recommended for production:
  - Rate limiting
  - Authentication
  - HTTPS
  - Database encryption

## Contacts

`Adedoyin Simeon Adeyemi` | [LinkedIn](https://www.linkedin.com/in/adedoyin-adeyemi-a7827b160/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For questions or support, please [open an issue](https://github.com/yourusername/incidence_response_plan_health/issues) on GitHub.