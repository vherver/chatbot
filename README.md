# Chatbot Debate API

This project is a **Django + DRF** API containerized with Docker.  
It provides a chatbot that debates with the user based on a topic and stance inferred from messages.  
It also includes **Swagger documentation** and a **Postman collection** for easy testing.

---

## 📦 Requirements
- Docker & Docker Compose  
- Python 3.12 (only required if running locally without Docker)  

---

## ⚙️ Makefile Commands

The project provides a `Makefile` to simplify common operations:

```bash
make             # Show all available commands
make install     # Install requirements and build Docker images
make run         # Run the service + dependencies (e.g. Postgres)
make test        # Run tests inside Docker
make down        # Stop running services
make clean       # Stop and remove containers, networks, volumes
```
---
## 🧪 Running Tests & Coverage

To execute all tests:

```bash
make test
```

---
## 📊 Test Coverage

```python
coverage report -m
```

| File                         | Stmts | Miss | Cover | Missing |
|------------------------------|-------|------|-------|---------|
| chatbot/__init__.py          | 0     | 0    | 100%  | -       |
| chatbot/settings.py          | 24    | 0    | 100%  | -       |
| chatbot/urls.py              | 8     | 0    | 100%  | -       |
| conversation/__init__.py     | 0     | 0    | 100%  | -       |
| conversation/apps.py         | 4     | 0    | 100%  | -       |
| conversation/models.py       | 35    | 0    | 100%  | -       |
| conversation/serializer.py   | 19    | 0    | 100%  | -       |
| conversation/urls.py         | 3     | 0    | 100%  | -       |
| conversation/views.py        | 50    | 0    | 100%  | -       |
| lms/__init__.py              | 21    | 0    | 100%  | -       |
| **TOTAL**                    | 164   | 0    | **100%** | -   |

## 🚀 Deployment

Example deployed URL:  
👉 [Heroku](https://chatbot-herver-4232679316c7.herokuapp.com/)

---

## 🛠️ Tech Stack
- **Django 5** + **Django REST Framework**  
- **PostgreSQL** (Dockerized, or AWS RDS in production)  
- **Swagger (drf-yasg)** for API documentation  
- **OpenAI Client** integration  
- **Docker + Docker Compose** for containerization  
- **Coverage + Pytest/Django Test Runner** for testing
- **flake8** for linting (code style checks)  
- **black** for automatic code formatting  
---

