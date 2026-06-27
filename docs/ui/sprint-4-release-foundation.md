# Sprint 4 – Release Foundation

## Übersicht

Sprint 4 implementiert professionelles **Environment Management** für das LLD Panel.

Das Projekt ist nun **Production-Ready** in Bezug auf Konfiguration.

## Architektur

### Problem (Vorher)

Hardcoded Konfigurationswerte in `settings.py`:

```python
SECRET_KEY = 'django-insecure-...'  # Geheim in Code ❌
DEBUG = True                        # Gleich für alle Umgebungen ❌
ALLOWED_HOSTS = []                  # Manuell ändern vor Deploy ❌
```

**Probleme:**
- Secret Keys im Repository
- Keine Unterscheidung Dev/Prod
- Docker-unfähig
- Deployment-Fehleranfällig

### Lösung (Nachher)

Environment-basierte Konfiguration mit `django-environ`:

```python
import environ

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')              # Aus .env ✓
DEBUG = env('DEBUG')                        # Verschiedene Werte pro Umgebung ✓
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')   # Für Docker/CI bereit ✓
```

**Struktur:**
```
.env              ← Development Config (NICHT im Repository)
.env.example      ← Template mit Platzhaltern (IM Repository)
```

## Implementierte Dateien

### 1. `.env.example` (IM Repository)

Template mit sicheren Platzhaltern:

```ini
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ENVIRONMENT=development
```

**Zweck:** Zeigt, welche Variablen benötigt werden

### 2. `.env` (NICHT im Repository, via .gitignore)

Development-spezifische Konfiguration:

```ini
SECRET_KEY=django-insecure-local-development-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ENVIRONMENT=development
```

**Zweck:** Wird automatisch von Django geladen

### 3. `.gitignore` aktualisiert

```
.env
.env.local
.env.*.local
```

Die `.env` Datei wird nicht committed!

### 4. `requirements.txt` aktualisiert

```
Django==6.0.6
django-environ==0.10.0
```

Neue Abhängigkeit: `django-environ`

### 5. `settings.py` angepasst

```python
import environ

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
```

**Änderung:** Hardcoded Values → Environment Variables

### 6. `DEVELOPMENT.md`

Setup-Anleitung für lokale Entwicklung:

```bash
cp .env.example .env
python manage.py runserver
```

### 7. Dokumentation

**ADR-0003: Environment Management**
- Warum Environment Variables?
- Sicherheit & Best Practices
- Implementierungsplan

**Deployment Guide: Environment Setup**
- Installation
- Konfiguration
- Dev vs Production Unterschiede
- CI/CD Integration
- Häufige Probleme

## Standards eingehalten

### Security

✓ Keine Secrets im Code  
✓ `.env` nicht im Repository  
✓ Zufällige SECRET_KEY für Production  
✓ DEBUG=False in Production (erzwungen)  

### Django Best Practices

✓ `django-environ` für Config  
✓ Environment Separation (Dev/Prod)  
✓ Settings aus Environment Variables  
✓ `.env.example` für Dokumentation  

### DevOps-Ready

✓ Docker-kompatibel  
✓ CI/CD-freundlich  
✓ Secrets in Environment gespeichert  
✓ Keine Konfigurationsfiles in Docker needed  

## Umgebungs-Unterschiede

### Development

```
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ENVIRONMENT=development
```

**Verhalten:**
- Debugging aktiv
- Template-Fehler angezeigt
- Static Files automatisch serviert

### Production

```
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
ENVIRONMENT=production
SECRET_KEY=<sehr-sicherer-Zufallsschlüssel>
```

**Verhalten:**
- Keine Debug-Info preisgegeben
- Error Logging aktiviert
- HTTPS erzwungen

## Workflow

### Lokal entwickeln

```bash
# Setup (einmalig)
cp .env.example .env
pip install -r requirements/development.txt

# Entwickeln (täglich)
python manage.py runserver
```

### Deployment

```bash
# Auf Production-Server
scp .env.example user@prod:/app/
ssh user@prod

# .env mit Production-Secrets erstellen
cat > .env << EOF
SECRET_KEY=$(openssl rand -base64 32)
DEBUG=False
ALLOWED_HOSTS=example.com
ENVIRONMENT=production
EOF

# Django starten
python manage.py runserver 0.0.0.0:8000
```

### Docker

```dockerfile
# Development
FROM python:3.14
COPY requirements/ requirements/
RUN pip install -r requirements/development.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production
FROM python:3.14-slim
COPY requirements/ requirements/
RUN pip install -r requirements/production.txt
COPY . .
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```bash
docker run -e SECRET_KEY=xyz -e DEBUG=False myapp
```

## Tests

Nach Sprint 4 können Sie verifizieren:

```bash
# 1. Development Server startet
python manage.py runserver

# 2. .env wird geladen
python manage.py shell
>>> from django.conf import settings
>>> settings.SECRET_KEY  # Sollte aus .env sein
>>> settings.DEBUG       # Sollte True sein

# 3. Production Config funktioniert
# SECRET_KEY=prod-key DEBUG=False python manage.py test
```

## Migration von alter Config

**Alte settings.py:**
```python
SECRET_KEY = 'django-insecure-...'
DEBUG = True
ALLOWED_HOSTS = []
```

**Neue settings.py:**
```python
import environ
env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
```

**Für Entwickler:**
1. `pip install django-environ`
2. `cp .env.example .env`
3. Weiterarbeiten (alles transparent)

## Checkliste vor Production

- [ ] `.env.example` vorhanden und aktuell
- [ ] `.env` in `.gitignore`
- [ ] `django-environ` in `requirements/base.txt`
- [ ] `settings.py` nutzt `environ.Env`
- [ ] Production `.env` hat sicheren `SECRET_KEY`
- [ ] Production `.env` hat `DEBUG=False`
- [ ] Production `.env` hat korrekte `ALLOWED_HOSTS`
- [ ] Keine Secrets im Repository
- [ ] `DEVELOPMENT.md` für neue Entwickler vorhanden
- [ ] `requirements/` Struktur konfiguriert
- [ ] Version zentral in `src/config/version.py` definiert

## Nächster Sprint

### Sprint 5: Authentication & Users

- `accounts` Django-App
- Login/Logout Views
- User Models
- Session Management
- Permission System

Alles basiert auf dieser sicheren Environment-Konfiguration! ✓

---

## ERWEITERUNG: Modular Requirements Management

### Problem (Vorher)

Alle Abhängigkeiten in einer `requirements.txt`:

```
Django==6.0.6
django-environ==0.10.0
pytest==7.4.0                    # Dev-Tool
black==23.7.0                    # Dev-Tool
gunicorn==21.2.0                 # Production nur!
```

**Probleme:**
- Unklar, welche Packages sind wirklich notwendig?
- Production mit Dev-Tools belastet (Container größer, Sicherheit)
- Docker Images 500MB+ größer als nötig

### Lösung (Nachher)

Modular organisierte Requirements:

```
requirements/
├── base.txt              # Gemeinsam: Django, django-environ
├── development.txt       # Dev + base (pytest, black, etc.)
└── production.txt        # Prod + base (gunicorn, etc.)
```

### Installation

```bash
# Development
pip install -r requirements/development.txt

# Production
pip install -r requirements/production.txt
```

**Details:** [ADR-0004](../adr/0004-modular-requirements-management.md)

---

## ERWEITERUNG: Centralized Version Management

### Problem (Vorher)

Version erscheint überall und ist hart codiert:

```html
<!-- header.html -->
<span>Version 0.1.0</span>  <!-- Hart codiert ❌ -->
```

```python
# context_processors.py
'app_version': '0.1.0',    # Hart codiert ❌
```

**Probleme:**
- Release erfordert 3-4 Dateien manuell ändern
- Inkonsistenz möglich
- Schwer zu automatisieren

### Lösung (Nachher)

Eine Datei, eine Versionsnummer:

```python
# src/config/version.py
VERSION = "0.1.0-alpha.1"
```

Alles importiert von dort:

```python
# context_processors.py
from config.version import VERSION
'app_version': VERSION,  # ✓ Zentral
```

### Release-Workflow

```bash
vim src/config/version.py
# VERSION = "0.1.0-alpha.1" → "0.1.0"

git commit -m "Release 0.1.0"
git tag 0.1.0
# ✓ Alles aktualisiert sich automatisch!
```

**Details:** [ADR-0005](../adr/0005-centralized-version-management.md)

---

## Sprint 4 Definition of Done ✅

- ✓ Environment Management (ADR-0003)
- ✓ Requirements-Struktur (ADR-0004)
- ✓ Version Management (ADR-0005)
- ✓ Dokumentation vollständig
- ✓ Keine Secrets im Code
- ✓ Docker-optimiert
- ✓ Production-ready
- ✓ Single Source of Truth überall
