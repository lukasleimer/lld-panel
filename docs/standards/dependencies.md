# Dependencies Management

## Struktur

```
requirements/
├── base.txt              # Gemeinsame Abhängigkeiten (alle Umgebungen)
├── development.txt       # Dev-spezifische Tools
└── production.txt        # Production-spezifische Packages
```

## Installation

### Development (lokal)

```bash
pip install -r requirements/development.txt
```

**Includes:**
- Django
- django-environ
- Testing Tools (pytest, pytest-django)
- Debugging (django-debug-toolbar)
- Code Quality (black, flake8)

### Production

```bash
pip install -r requirements/production.txt
```

**Includes:**
- Django
- django-environ
- Production WSGI Server (gunicorn)
- Optional: Database Driver (psycopg2 für PostgreSQL)

### Basis nur (CI/CD, Testing)

```bash
pip install -r requirements/base.txt
```

## Warum aufgeteilt?

### Klarheit

- **base.txt:** Was ist wirklich notwendig?
- **development.txt:** Was braucht nur Entwickler?
- **production.txt:** Was ist nur für Live-Umgebungen?

### Container-Größe

- Production Image ohne Dev-Tools: **500MB+ kleiner**
- Weniger dependencies = schneller starten
- Bessere Security (weniger Angriffsfläche)

### Django Best Practice

Diese Struktur ist Standard in der Django-Community:
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [Wagtail CMS](https://github.com/wagtail/wagtail)
- [Django Cookiecutter](https://github.com/cookiecutter/cookiecutter-django)

## Abhängigkeiten

### base.txt

```
Django==6.0.6              # Web Framework
django-environ==0.10.0     # Environment Variables
```

### development.txt

```
-r base.txt

# Testing
pytest==7.4.0
pytest-django==4.5.2

# Code Quality
black==23.7.0
flake8==6.0.0

# Debugging
django-debug-toolbar==4.1.0

# Optional: Coverage
coverage==7.2.0
```

### production.txt

```
-r base.txt

# WSGI Server
gunicorn==21.2.0

# Database
psycopg2-binary==2.9.6

# Optional: Security
django-cors-headers==4.2.0
```

## Upgrade & Maintenance

### Einzelnes Package upgraden

```bash
pip install --upgrade django
pip freeze > requirements/base.txt
```

### Alle Packages upgraden

```bash
pip install --upgrade -r requirements/base.txt
pip freeze > requirements/base.txt
```

## Docker

### Dockerfile.dev

```dockerfile
FROM python:3.14
WORKDIR /app
COPY requirements/ requirements/
RUN pip install -r requirements/development.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Dockerfile.prod

```dockerfile
FROM python:3.14-slim  # Schlankeres Image
WORKDIR /app
COPY requirements/ requirements/
RUN pip install -r requirements/production.txt
COPY src/ src/
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Related Documentation

- [ADR-0004: Modular Requirements Management](../adr/0004-modular-requirements-management.md)
- [Deployment Guide](./environment-setup.md)
- [Development Setup](../../DEVELOPMENT.md)

## FAQ

**Q: Warum drei Dateien statt zwei?**
A: `base.txt` dokumentiert explizit die gemeinsamen Abhängigkeiten. Das macht das Projekt wartbarer und skaliert besser (später: testing.txt, docs.txt, etc.)

**Q: Kann ich alle zusammen installieren?**
A: Ja: `pip install -r requirements/base.txt -r requirements/development.txt`
Oder nutze einfach: `pip install -r requirements/development.txt` (includes base)

**Q: Was ist mit requirements.lock?**
A: Nicht nötig für diese Projektgröße. Später evtl. pip-tools oder Poetry.
