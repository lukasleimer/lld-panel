# Deployment & Configuration

## Environment Variables

Das LLD Panel nutzt **Environment Variables** zur Konfiguration. Dies ist der Django Best Practice Standard.

### Warum Environment Variables?

**Sicherheit:**
- Secrets (SECRET_KEY, API Keys) bleiben nicht im Code
- `.env` Datei ist nicht im Repository
- Verschiedene Secrets für Dev/Prod

**Flexibilität:**
- Gleicher Code für alle Umgebungen
- Konfiguration zur Laufzeit änderbar
- Docker-kompatibel

**Best Practice:**
- Django empfiehlt dies offiziell
- Folgt der 12-Factor App Methodology
- Standard bei Deployment-Tools (Heroku, AWS, etc.)

## Installation

### Development

```bash
pip install -r requirements/development.txt
```

### Production

```bash
pip install -r requirements/production.txt
```

### Basis (nur zum Testen)

```bash
pip install -r requirements/base.txt
```

**Details:** Siehe [docs/standards/dependencies.md](../standards/dependencies.md)

## Setup

### Schritt 1: .env Datei erstellen

Basierend auf `.env.example`:

```bash
cp .env.example .env
```

### Schritt 2: .env anpassen

```ini
SECRET_KEY=your-random-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ENVIRONMENT=development
```

### Schritt 3: settings.py konfigurieren

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

## Konfigurationsoptionen

### Basis (Development)

```ini
SECRET_KEY=your-development-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ENVIRONMENT=development
```

### Production

```ini
SECRET_KEY=<sehr-sicherer-zufälliger-key>
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
ENVIRONMENT=production
```

### Zukünftig (Database)

```ini
DATABASE_URL=postgresql://user:password@localhost:5432/lld_panel
```

## Environment Unterschiede

### Development

```
DEBUG=True           # Debugging-Informationen
ALLOWED_HOSTS=localhost,127.0.0.1  # Nur Localhost
ENVIRONMENT=development
```

**Verhalten:**
- Django Debug Toolbar aktiv
- Template-Fehler angezeigt
- Static Files automatisch serviert

### Production

```
DEBUG=False          # Keine Debug-Info!
ALLOWED_HOSTS=example.com,www.example.com  # Production Domain
ENVIRONMENT=production
```

**Verhalten:**
- Error Logs statt Debug-Seite
- Static Files müssen deployed sein
- HTTPS erzwungen
- CSRF Protection aktiv

## .gitignore

**Die `.env` Datei darf NICHT committed werden!**

```
# Environment
.env
.env.local
.env.*.local
```

## Workflow

### Lokal entwickeln

```bash
# 1. .env erstellen
cp .env.example .env

# 2. Werte für Local Development setzen
# nano .env

# 3. Development Server starten
python manage.py runserver
# Django lädt automatisch .env
```

### Deployment (Production)

```bash
# Auf Production-Server
scp .env.example user@production:/app/

# SSH auf Server
ssh user@production

# .env erstellen und anpassen
cat .env.example > .env
nano .env  # Secrets setzen

# Django starten
python manage.py runserver 0.0.0.0:8000
```

### Docker

```dockerfile
FROM python:3.14

WORKDIR /app

# .env.example im Container
COPY .env.example .env

# Secrets via Umgebungsvariablen (Runtime)
RUN pip install django-environ

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

```bash
docker run -e SECRET_KEY=xyz -e DEBUG=False myapp
```

## Häufige Probleme

### ".env Datei nicht gefunden"

```
FileNotFoundError: [Errno 2] No such file or directory: '.env'
```

**Lösung:** `.env.example` → `.env` kopieren

```bash
cp .env.example .env
```

### SECRET_KEY ist leer

Sicherstellen, dass SECRET_KEY in `.env` gesetzt ist:

```ini
SECRET_KEY=some-random-string-here
```

Nicht leer lassen!

### ALLOWED_HOSTS Fehler

```
DisallowedHost: Invalid HTTP_HOST header: 'example.com'
```

`.env` sollte die Domain enthalten:

```ini
ALLOWED_HOSTS=example.com,www.example.com
```

## Environment Variablen erzeugen

### Zufälligen SECRET_KEY generieren

```bash
# Linux/Mac
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# oder
openssl rand -base64 32
```

### In .env einfügen

```bash
echo "SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" > .env
```

## CI/CD Integration (GitHub Actions)

```yaml
name: Deploy

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Create .env
        run: |
          echo "SECRET_KEY=${{ secrets.DJANGO_SECRET_KEY }}" >> .env
          echo "DEBUG=False" >> .env
          echo "ALLOWED_HOSTS=${{ secrets.PRODUCTION_HOSTS }}" >> .env
      
      - name: Deploy
        run: |
          # Deploy commands
```

## Best Practices

✓ `.env.example` im Repository  
✓ `.env` nicht committed  
✓ SECRET_KEY niemals im Code  
✓ Verschiedene Secrets pro Umgebung  
✓ Secrets in CI/CD Secrets Store  
✓ `.env` in Production über Deployment-Tool  

## Checkliste vor Deployment

- [ ] `.env` vorhanden und gefüllt
- [ ] `SECRET_KEY` ist ein zufälliger String
- [ ] `DEBUG=False` in Production
- [ ] `ALLOWED_HOSTS` enthält Production Domain
- [ ] `.env` ist in `.gitignore`
- [ ] `.env.example` ist aktuell
- [ ] Keine Secrets im Code oder Repository
