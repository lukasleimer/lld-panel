# ADR-0004: Modular Requirements Management

**Status:** Accepted  
**Date:** 2026-06-27  
**Author:** LLD Panel Team  

## Context

Das Projekt benötigt Abhängigkeiten für unterschiedliche Umgebungen:

- **Development:** Django, Testing Tools, Debugging, Linting
- **Production:** Django, Production WSGI Server, Performance Tools
- **Basis:** Gemeinsame Packages für alle Umgebungen

Aktuell: Alle Abhängigkeiten in einer `requirements.txt` vermischt.

**Problem:**
- Unklare Abhängigkeiten (welche sind wirklich notwendig?)
- Production Umgebung wird mit Dev-Tools belastet
- Container-Images größer als nötig
- Schwer zu warten und zu verstehen

## Decision

**Implementiere modular organisierte Requirements-Dateien:**

```
requirements/
├── base.txt              # Gemeinsame Abhängigkeiten
├── development.txt       # Dev-spezifisch
└── production.txt        # Production-spezifisch
```

**Struktur:**
```
# requirements/base.txt
Django==6.0.6
django-environ==0.10.0

# requirements/development.txt
-r base.txt
pytest==7.4.0
pytest-django==4.5.2
black==23.7.0
flake8==6.0.0
django-debug-toolbar==4.1.0

# requirements/production.txt
-r base.txt
gunicorn==21.2.0
psycopg2-binary==2.9.6
django-cors-headers==4.2.0
```

## Rationale

### 1. **Klarheit (Dokumentation als Code)**
- `base.txt`: Sofort klar, welche Packages wirklich notwendig sind
- `development.txt`: Dev-Tools isoliert
- `production.txt`: Nur für Production relevant

### 2. **Container-Optimierung**
- Dev-Tools nicht in Production Images (Größe: 500MB+ gespart)
- Security: Weniger dependencies = kleinere Angriffsflache
- Performance: Schneller starten, weniger RAM

### 3. **Deployment-Clarität**
```bash
# Development
pip install -r requirements/development.txt

# Production
pip install -r requirements/production.txt

# CI/CD
pip install -r requirements/base.txt && pytest
```

### 4. **Django Best Practices**
- Empfohlenes Pattern in Django Community
- Entspricht Struktur großer Projects (Django Packages, Wagtail, etc.)
- Professioneller Standard

### 5. **Zukünftige Skalierung**
Leicht erweiterbar:
```
requirements/
├── base.txt
├── development.txt
├── production.txt
├── testing.txt        # Später: separates Testing Setup
├── docs.txt           # Später: Sphinx, etc.
└── ci.txt             # Später: Linting, Coverage Tools
```

## Implementation

### Dateistruktur

```
requirements/
├── base.txt
├── development.txt
└── production.txt
```

### Verwendung

```bash
# Local Development
pip install -r requirements/development.txt

# Production Deployment
pip install -r requirements/production.txt

# Testing nur
pip install -r requirements/base.txt && pytest

# CI/CD
pip install -r requirements/development.txt && pytest
```

### Docker

```dockerfile
# Dockerfile.dev
FROM python:3.14
COPY requirements/base.txt requirements/development.txt ./requirements/
RUN pip install -r requirements/development.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Dockerfile.prod
FROM python:3.14-slim  # Schlankeres Base Image
COPY requirements/base.txt requirements/production.txt ./requirements/
RUN pip install -r requirements/production.txt
CMD ["gunicorn", "config.wsgi:application"]
```

### Alte requirements.txt

**Option 1:** Durch `README.md` ersetzen
```markdown
## Installation

### Development
pip install -r requirements/development.txt

### Production
pip install -r requirements/production.txt
```

**Option 2:** Keep als Convenience (verweis auf development.txt)
```
# Veraltet! Nutze stattdessen:
# pip install -r requirements/development.txt
-r requirements/development.txt
```

**Wir wählen: Entfernung** (sauberer, kein veralteter Code)

## Affected Files

- Neue: `requirements/base.txt`
- Neue: `requirements/development.txt`
- Neue: `requirements/production.txt`
- Gelöscht: `requirements.txt`
- Geändert: `DEVELOPMENT.md` (neue Installationsbefehle)
- Geändert: `docs/deployment/environment-setup.md` (neue Befehle)

## Migration Path

### Für Bestehende Developer

```bash
# Alt
pip install -r requirements.txt

# Neu
pip install -r requirements/development.txt
```

**Einfache Migration:** Besteht nur aus Befehls-Anpassung

### Für CI/CD

```yaml
# Alt
pip install -r requirements.txt && pytest

# Neu
pip install -r requirements/development.txt && pytest
```

**oder optimal:**
```yaml
pip install -r requirements/base.txt && pytest
```

## Alternatives Considered

### 1. Pip-tools (pip-compile)
**Verworfen:** Zu komplex für diese Projektgröße
- Würde `requirements.lock` Dateien brauchen
- Overhead für 2-3 Packages

### 2. Poetry (Poetry-Lock)
**Verworfen:** Unterschiedliches Tool-Ecosystem
- Nicht Standard in Django-Projekten
- Migration später komplexer

### 3. Alles in einer Datei (Status Quo)
**Verworfen:** Weniger Klarheit

## Success Criteria

- ✓ Requirements logisch aufgeteilt
- ✓ Development und Production haben unterschiedliche Dependencies
- ✓ Container Images sind kleiner
- ✓ Documentation ist klar
- ✓ Migration für Developer einfach

## Related

- ADR-0003: Environment Management
- docs/standards/dependencies.md (neu)
- docs/deployment/docker.md (geplant)

## References

- [Django Project Layout](https://docs.djangoproject.com/en/stable/)
- [Two Scoops of Django: Requirements Files](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [Wagtail Project Structure](https://github.com/wagtail/wagtail)
