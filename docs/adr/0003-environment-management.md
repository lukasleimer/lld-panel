# ADR-0003: Environment Management

**Status:** ANGENOMMEN  
**Datum:** 2026-06-27  
**Entscheidung:** Verwende `django-environ` für Environment-basierte Konfiguration

## Kontext

Aktuell sind Konfigurationswerte in `settings.py` hardcoded:

```python
SECRET_KEY = 'django-insecure-b=&g&mgclsdx=@_)dcwj)(tqhm36reokmt_#ys=nsn70a5g(ta'
DEBUG = True
ALLOWED_HOSTS = []
```

Das ist ein **Sicherheitsrisiko** für mehrere Gründe:

1. **Secret Keys im Repository** – Jeder, der den Code hat, kennt den Secret Key
2. **Keine Unterscheidung zwischen Umgebungen** – Dev/Staging/Production nutzen gleiche Config
3. **Keine Docker-Unterstützung** – Container brauchen dynamische Config
4. **Deployment-Probleme** – Konfiguration muss vor jedem Deploy manuell angepasst werden

## Anforderungen

✓ **Sicherheit** – Secrets nicht im Repository  
✓ **Flexibilität** – Verschiedene Configs für Dev/Prod  
✓ **Docker-Ready** – Environment Variablen für Container  
✓ **Django Best Practices** – Bewährte Patterns  
✓ **Einfachheit** – Minimal invasive Änderungen  

## Entscheidung

**Wir verwenden `django-environ`** für Environment-basierte Konfiguration.

### Paket

```
pip install django-environ
```

Kleine, fokussierte Bibliothek speziell für Django-Konfiguration.

### Struktur

```
.env              ← Development Config (NICHT im Repository!)
.env.example      ← Template mit Platzhaltern (IM Repository)
```

### settings.py

```python
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env()  # Liest .env

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost'])
```

## Rationale

### 1. Sicherheit

**Vorher:**
```python
SECRET_KEY = 'django-insecure-...'  # Im Repository sichtbar!
```

**Nachher:**
```python
SECRET_KEY = env('SECRET_KEY')  # Aus .env, nicht im Repository
```

Der Secret Key ist geheim.

### 2. Umgebungs-Unterschied

**.env.development**
```
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

**.env.production**
```
DEBUG=False
ALLOWED_HOSTS=example.com
DATABASE_URL=postgresql://user:password@host/db
SECRET_KEY=<sehr-sicherer-zufalliger-key>
```

Gleicher Code, verschiedene Config.

### 3. Docker-Ready

Docker setzt Environment Variablen:

```bash
docker run -e SECRET_KEY=xyz -e DEBUG=False myapp
```

Oder via `.env` Datei:

```bash
docker run --env-file .env.production myapp
```

### 4. Deployment-Automation

CI/CD Tools können `.env` Datei dynamisch generieren:

```yaml
# GitHub Actions
- name: Create .env
  run: |
    echo "SECRET_KEY=${{ secrets.DJANGO_SECRET_KEY }}" >> .env
    echo "DEBUG=False" >> .env
    echo "ALLOWED_HOSTS=${{ secrets.ALLOWED_HOSTS }}" >> .env
```

### 5. Django Best Practices

Die Django-Dokumentation empfiehlt:

> "The Secret Key should be a large random value and it should never be committed to version control."

Wir folgen diesem Standard.

## Implementierung

### Installation

```bash
pip install django-environ
```

### settings.py

```python
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
```

### .env.example

```ini
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (für zukünftige Nutzung)
DATABASE_URL=sqlite:///db.sqlite3

# Environment
ENVIRONMENT=development
```

### .env (im Development)

```ini
SECRET_KEY=<zufällig-generierter-key>
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### .gitignore

```
.env
.env.local
.env.*.local
```

Die `.env` Datei wird NICHT committed!

## Umgebungs-Unterschiede

### Development

```
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Staging

```
DEBUG=False
ALLOWED_HOSTS=staging.example.com
DATABASE_URL=postgresql://user:pass@staging-db/lld
SECRET_KEY=<random-secure-key>
```

### Production

```
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
DATABASE_URL=postgresql://user:pass@prod-db/lld
SECRET_KEY=<random-secure-key>
HTTPS_REDIRECT=True
SECURE_SSL_REDIRECT=True
```

## Workflow

### Lokal (Development)

1. `.env` Datei erstellen (basierend auf `.env.example`)
2. Werte anpassen für Lokal-Entwicklung
3. `.env` wird von Django automatisch geladen

```bash
# Copy template
cp .env.example .env

# Edit for local development
nano .env
```

### Deployment

1. `.env.example` im Repository
2. Deployment-Prozess erstellt `.env` auf Server
3. Django lädt Konfiguration automatisch

```bash
# On server
echo "SECRET_KEY=$(openssl rand -base64 32)" >> .env
echo "DEBUG=False" >> .env
echo "ALLOWED_HOSTS=example.com" >> .env
```

## Migration

### Alte Config

```python
SECRET_KEY = 'django-insecure-...'
DEBUG = True
ALLOWED_HOSTS = []
```

### Neue Config

```python
import environ

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY', default='django-insecure-...')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
```

Mit `default` Werten für Backward Compatibility.

## Best Practices eingehalten

✓ Keine Secrets im Code  
✓ `.env` nicht im Repository  
✓ `.env.example` für Dokumentation  
✓ Django-Konvention  
✓ Docker-kompatibel  
✓ CI/CD-freundlich  
✓ Skalierbar auf Production  

## Zukünftige Erweiterungen

Später können wir hinzufügen:

```python
# Database URL
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600
    )
}

# Email Configuration
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='localhost')
EMAIL_PORT = env.int('EMAIL_PORT', default=1025)

# Redis Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://127.0.0.1:6379/1'),
    }
}
```

Alles über Environment Variablen konfigurierbar.

## Gültig ab

27.06.2026

---

**Entscheidung getroffen von:** Entwicklerteam  
**Nächste Überprüfung:** Nach erstem Production-Deployment
