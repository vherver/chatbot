# 🤖 Chatbot Debate API  

[![Tests](https://github.com/herver/chatbot/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/herver/chatbot/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/herver/chatbot/branch/main/graph/badge.svg)](https://codecov.io/gh/herver/chatbot)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Django](https://img.shields.io/badge/django-5.0-green.svg)
[![Heroku](https://img.shields.io/badge/deployed-Heroku-7056bf.svg)](https://chatbot-herver-4232679316c7.herokuapp.com/)


This is a Django 5 + Django REST Framework project that provides an API for starting and managing debate-style conversations with an AI bot powered by OpenAI.


This project is a **Django + DRF** API containerized with Docker.  
It provides a chatbot that debates with the user based on a topic and stance inferred from messages.  
It also includes **Swagger documentation** and a **Postman collection** for easy testing.

---

## 📦 Requirements
- Docker & Docker Compose  
- Python 3.12 (only required if running locally without Docker)  

---

## 🔑 Environment Variables

The application uses a `.env` file to manage secrets and database configuration.  

- `.env.example` is included in the repo as a template.  
- The **real `.env` file will be provided by email in a `.zip`**.  
- You must copy `.env.example` → `.env` and adjust values accordingly.  

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

```bash
pytest --cov=. --cov-report=term-missing
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
| conversation/views.py        | 52    | 0    | 100%  | -       |
| lms/__init__.py              | 21 7  | 0    | 100%  | -       |
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

