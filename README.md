# URL Shortener API

![Project Poster](screenshots/poster.png)

---

## 2. Project Badges

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063)
![pytest](https://img.shields.io/badge/pytest-Testing-0A9EDC)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-PASS-success)

---

## 3. Screenshots

### Frontend

![Frontend](screenshots/frontend.PNG)

Main URL Shortener frontend.

### Custom Alias

![Custom Alias](screenshots/frontend-new-alias.PNG)

Creating a shortened URL using a custom alias.

### URL Analytics

![URL Analytics](screenshots/frontend-analytics.PNG)

Viewing click analytics for an existing short URL.

### Database Click Count

![Database Click Count](screenshots/neon-alias-click-count.PNG)

Database verification of recorded URL clicks.

### Database Record

![Database Record](screenshots/neon-record-created.PNG)

Database verification of the created URL record.

### Swagger API

![Swagger API](screenshots/swagger-home.PNG)

FastAPI Swagger/OpenAPI interface.

### Custom Alias Response

![Custom Alias Response](screenshots/swagger-custom-alias-response.PNG)

Successful custom alias creation through the API.

### Duplicate Alias Error

![Duplicate Alias Error](screenshots/swagger-duplicate-url-error.PNG)

API response when a custom alias is already in use.

---

## 4. Project Title

# URL Shortener API

**Project ID:** 018

A REST API and browser-based frontend for creating, managing, redirecting, and analyzing shortened URLs.

---

## 5. Project Overview

### Purpose

The URL Shortener API converts long URLs into compact, shareable URLs and provides URL lifecycle management and click analytics.

### Problem Solved

Long URLs can be difficult to share and manage.

This project provides a service for:

- Generating unique short URL codes
- Creating custom aliases
- Redirecting users to original destinations
- Recording successful clicks
- Viewing click analytics
- Managing URL activation and expiration

### Typical Use Cases

- Shareable links
- Campaign and tracking links
- Internal enterprise tools
- SaaS applications
- API development
- Backend engineering demonstrations

---

## 6. Features

### URL Creation

- Create shortened URLs from long URLs.
- Automatically generate unique short codes.
- Support custom aliases.
- Support optional expiration timestamps.
- Return a complete short URL.

### URL Redirection

- Resolve short URL identifiers.
- Redirect users to the original destination.
- Record successful clicks.
- Prevent redirection of inactive URLs.
- Prevent redirection of expired URLs.

### URL Analytics

- View total click count.
- View first click timestamp.
- View last click timestamp.
- Look up analytics using a short URL identifier.
- Refresh analytics from the frontend.

### URL Lifecycle

- Retrieve URL details.
- Activate URLs.
- Deactivate URLs.
- Soft-delete URLs.
- Detect expired URLs.
- Prevent invalid lifecycle transitions.

### Validation and Error Handling

- Validate HTTP URLs.
- Validate custom aliases.
- Detect duplicate aliases.
- Handle application-specific errors.
- Return appropriate HTTP status codes.

### Frontend

- Create shortened URLs.
- Enter custom aliases.
- Set optional expiration.
- Copy generated short URLs.
- Look up analytics for an existing short URL.
- Refresh analytics.

### API Documentation

Interactive API documentation is available through FastAPI Swagger/OpenAPI.

---

## 7. Technology Stack

| **Technology** | **Purpose** |
| -------------- | ----------- |
| Python 3.14 | Application development |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database access |
| Pydantic | Request and response validation |
| pytest | Automated testing |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend API integration |
| Git | Version control |
| GitHub | Source-code repository |

---

## 8. Project Structure

The repository is organized into API routes, URL business logic, database services, data models, frontend assets, tests, documentation, and release artifacts.

```text
018 URL Shortener API/
│
├── .github/
├── .vscode/
│
├── assets/
│   ├── fonts/
│   ├── icons/
│   ├── images/
│   └── templates/
│
├── data/
│   ├── input/
│   ├── output/
│   └── samples/
│
├── docs/
│   └── UserGuide.md
│
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
│
├── logs/
│   └── execution_report.txt
│
├── releases/
│   ├── latest/
│   ├── v1.0/
│   └── v1.1/
│
├── screenshots/
│   ├── frontend-analytics.PNG
│   ├── frontend-new-alias.PNG
│   ├── frontend.PNG
│   ├── neon-alias-click-count.PNG
│   ├── neon-record-created.PNG
│   ├── poster.png
│   ├── swagger-custom-alias-response.PNG
│   ├── swagger-duplicate-url-error.PNG
│   └── swagger-home.PNG
│
├── src/
│   ├── api/
│   │   ├── health_routes.py
│   │   ├── redirect_routes.py
│   │   └── url_routes.py
│   │
│   ├── core/
│   │   └── url/
│   │       ├── alias_validator.py
│   │       ├── click_recorder.py
│   │       ├── short_code_generator.py
│   │       ├── url_analytics.py
│   │       ├── url_creator.py
│   │       ├── url_lifecycle.py
│   │       └── url_redirector.py
│   │
│   ├── models/
│   │   ├── analytics_schema.py
│   │   ├── click_model.py
│   │   ├── url_model.py
│   │   └── url_schema.py
│   │
│   ├── services/
│   │   ├── click_repository.py
│   │   ├── database_service.py
│   │   └── url_repository.py
│   │
│   ├── ui/
│   │
│   ├── utils/
│   │   └── logger.py
│   │
│   └── config.py
│
├── tests/
│   └── test_url_lifecycle.py
│
├── .env
├── .gitignore
├── LICENSE
├── main.py
├── pyproject.toml
├── README.md
└── requirements.txt
```

Generated artifacts such as `__pycache__`, `*.pyc`, and `.pytest_cache` are intentionally excluded from the documented source structure.

---

## 9. Module Overview

| **Module** | **Responsibility** |
| ---------- | ------------------- |
| `api` | Defines FastAPI HTTP routes and maps application errors to HTTP responses. |
| `core/url` | Contains URL business logic including creation, validation, redirection, analytics, click recording, and lifecycle management. |
| `services` | Provides database sessions and repository-based persistence operations. |
| `models` | Defines SQLAlchemy database models and Pydantic API schemas. |
| `utils` | Provides shared application utilities such as logging. |
| `frontend` | Provides the browser interface for URL creation, short URL display, and analytics lookup. |
| `tests` | Contains automated tests. |
| `config.py` | Provides application configuration and environment-based settings. |

### Architecture

The application follows a layered architecture:

```text
Browser
   │
   ▼
Frontend
   │
   │ HTTP Requests
   ▼
FastAPI Routes
   │
   ▼
Core Business Logic
   │
   ▼
Repositories / Database Services
   │
   ▼
PostgreSQL
```

This separation keeps HTTP handling, business rules, persistence, data models, and frontend presentation independent.

---

## 10. Source Code Overview

### Application Entry Point

| **Source File** | **Purpose** | **Dependencies** |
| --------------- | ----------- | ---------------- |
| `main.py` | Creates and starts the FastAPI application and registers the API routes. | FastAPI, Uvicorn |
| `src/config.py` | Loads application configuration and environment-based settings. | Pydantic Settings |

### API Layer

| **Source File** | **Purpose** | **Dependencies** |
| --------------- | ----------- | ---------------- |
| `src/api/health_routes.py` | Provides the API health-check endpoint. | FastAPI |
| `src/api/redirect_routes.py` | Resolves public short identifiers and redirects users to the original destination. | FastAPI |
| `src/api/url_routes.py` | Provides endpoints for URL creation, retrieval, analytics, activation, deactivation, and deletion. | FastAPI, SQLAlchemy, Pydantic |

### Core Business Logic

| **Source File** | **Purpose** | **Dependencies** |
| --------------- | ----------- | ---------------- |
| `src/core/url/alias_validator.py` | Validates custom aliases and raises application-specific validation errors. | Python |
| `src/core/url/click_recorder.py` | Records successful URL clicks through the click repository. | ClickRepository |
| `src/core/url/short_code_generator.py` | Generates short URL codes when a custom alias is not supplied. | Python |
| `src/core/url/url_analytics.py` | Retrieves URL click analytics including total, first, and last clicks. | URLRepository, ClickRepository, Pydantic |
| `src/core/url/url_creator.py` | Implements URL creation including alias handling, short-code generation, expiration, persistence, and response construction. | URLRepository, ShortCodeGenerator, Pydantic |
| `src/core/url/url_lifecycle.py` | Handles URL retrieval, activation, deactivation, expiration checks, and soft deletion. | URLRepository |
| `src/core/url/url_redirector.py` | Resolves short identifiers, checks redirectability, records clicks, and returns the destination URL. | URLRepository, ClickRepository |

### Data Models

| **Source File** | **Purpose** | **Dependencies** |
| --------------- | ----------- | ---------------- |
| `src/models/analytics_schema.py` | Defines the API response model for URL click analytics. | Pydantic |
| `src/models/click_model.py` | Defines the database model for recorded URL clicks. | SQLAlchemy |
| `src/models/url_model.py` | Defines the database model for shortened URLs and lifecycle fields. | SQLAlchemy |
| `src/models/url_schema.py` | Defines API request and response schemas for URL operations. | Pydantic |

### Database Services

| **Source File** | **Purpose** | **Dependencies** |
| --------------- | ----------- | ---------------- |
| `src/services/database_service.py` | Creates the SQLAlchemy engine and manages database sessions and initialization. | SQLAlchemy |
| `src/services/url_repository.py` | Provides database operations for URL creation, lookup, update, and soft deletion. | SQLAlchemy |
| `src/services/click_repository.py` | Provides database operations for recording clicks and retrieving click aggregates. | SQLAlchemy |

### Utilities

| **Source File** | **Purpose** | **Dependencies** |
| --------------- | ----------- | ---------------- |
| `src/utils/logger.py` | Provides application logging and execution reporting. | Python logging |

### Frontend

| **Source File** | **Purpose** | **Dependencies** |
| --------------- | ----------- | ---------------- |
| `frontend/index.html` | Defines the browser interface for URL creation, short URL display, and analytics lookup. | HTML |
| `frontend/app.js` | Handles API requests, form submission, analytics lookup, refresh, and clipboard operations. | JavaScript Fetch API |
| `frontend/style.css` | Defines the visual layout, forms, buttons, messages, and analytics cards. | CSS |

### Tests

| **Source File** | **Purpose** | **Dependencies** |
| --------------- | ----------- | ---------------- |
| `tests/test_url_lifecycle.py` | Tests URL lifecycle behavior and state transitions. | pytest |

---

## 11. How to Run

### Prerequisites

- Python 3.14
- PostgreSQL
- Git

### Step 1 — Create a Virtual Environment

From the project root:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 2 — Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 3 — Configure Environment Variables

Create a `.env` file in the project root.

Configure the database connection and application settings required by the project.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/url_shortener
BASE_URL=http://localhost:8000
```

Do not commit the actual `.env` file to Git.

### Step 4 — Start PostgreSQL

Make sure PostgreSQL is running and the configured database is available.

### Step 5 — Start the Backend

From the project root:

```powershell
python main.py
```

The FastAPI backend runs at:

```text
http://localhost:8000
```

### Step 6 — Open Swagger

Open the following in a browser:

```text
http://localhost:8000/docs
```

### Step 7 — Start the Frontend

Open a second terminal.

Navigate to the frontend directory:

```powershell
cd frontend
```

Start the frontend server:

```powershell
python -m http.server 5500
```

Open:

```text
http://localhost:5500
```

### Runtime Architecture

```text
Browser
   │
   ├── Frontend
   │     http://localhost:5500
   │
   └── FastAPI Backend
         http://localhost:8000
                │
                ▼
           PostgreSQL
```

The frontend communicates with the FastAPI backend through HTTP requests.

---

## 12. How to Build

This project is a FastAPI web application with a browser-based frontend.

It is not packaged as a standalone desktop executable, therefore PyInstaller is not applicable.

### Run Backend

```powershell
python main.py
```

### Run Frontend

```powershell
cd frontend
python -m http.server 5500
```

The application is run by starting the backend API and serving the frontend separately.

---

## 13. Version

| **Item** | **Value** |
| -------- | --------- |
| Project ID | 018 |
| Current Version | 1.0.0 |
| Release Date | 13 August 2026 |
| Status | PASS |

---

## 14. Development Workflow

```text
Requirements
     ↓
Architecture & Project Structure
     ↓
Database & Data Models
     ↓
URL Creation
     ↓
Short Code & Alias Validation
     ↓
URL Redirect & Click Recording
     ↓
URL Analytics
     ↓
URL Lifecycle Management
     ↓
REST API
     ↓
Frontend Integration
     ↓
ESAT / API Testing
     ↓
Frontend Testing
     ↓
Documentation
     ↓
Git Repository
     ↓
GitHub Release
```

---

## 15. License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for the complete license text.

---

## 16. API Summary

| **Method** | **Endpoint** | **Purpose** |
| ---------- | ------------ | ----------- |
| `GET` | `/health` | Check API health |
| `POST` | `/api/v1/urls` | Create a shortened URL |
| `GET` | `/api/v1/urls/{url_id}` | Retrieve URL details |
| `GET` | `/api/v1/urls/{url_id}/analytics` | Retrieve analytics by URL ID |
| `PATCH` | `/api/v1/urls/{url_id}/activate` | Activate a URL |
| `PATCH` | `/api/v1/urls/{url_id}/deactivate` | Deactivate a URL |
| `DELETE` | `/api/v1/urls/{url_id}` | Soft-delete a URL |
| `GET` | `/{identifier}` | Redirect a short code or custom alias |

### API Documentation

Interactive Swagger documentation is available at:

```text
http://localhost:8000/docs
```

---

## Project Status

**Project 018 — URL Shortener API**

| **Area** | **Status** |
| -------- | ---------- |
| Backend API | Complete |
| PostgreSQL Integration | Complete |
| URL Creation | Complete |
| Custom Aliases | Complete |
| URL Redirection | Complete |
| Click Recording | Complete |
| URL Analytics | Complete |
| URL Lifecycle Management | Complete |
| Browser Frontend | Complete |
| Frontend Analytics Lookup | Complete |
| ESAT | Completed |
| Documentation | Complete |
