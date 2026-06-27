# Local Development Setup

## Erste Schritte

### 1. Repository klonen

```bash
git clone <repository-url>
cd lld-panel
```

### 2. Virtual Environment erstellen

```bash
python -m venv .venv
```

**Aktivieren:**
- Windows: `.venv\Scripts\Activate.ps1`
- Mac/Linux: `source .venv/bin/activate`

### 3. Dependencies installieren

```bash
pip install -r requirements/development.txt
```

### 4. Environment konfigurieren

```bash
# .env.example zu .env kopieren
cp .env.example .env

# .env öffnen und prüfen (standardwerte sind für Development OK)
# nano .env
```

Inhalt von `.env` sollte sein:

```ini
SECRET_KEY=django-insecure-local-development-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ENVIRONMENT=development
```

### 5. Django-Migrations durchführen

```bash
cd src
python manage.py migrate
```

### 6. Development Server starten

```bash
python manage.py runserver
```

Öffnen Sie: http://localhost:8000

## Projektstruktur

```
lld-panel/
├── .env                  ← Development Config (nicht committen!)
├── .env.example          ← Template
├── requirements.txt      ← Python Dependencies
├── src/
│   ├── config/           ← Django Config
│   ├── apps/             ← Django Apps
│   │   └── core/         ← Core Infrastructure
│   ├── templates/        ← Django Templates
│   ├── static/           ← CSS, JS, Images
│   └── manage.py
├── docs/                 ← Dokumentation
└── README.md
```

## Wichtige Befehle

### Development Server

```bash
python manage.py runserver
```

### Database Migrations

```bash
# Neue Migrations erstellen
python manage.py makemigrations

# Migrations durchführen
python manage.py migrate

# Migration Status
python manage.py showmigrations
```

### Django Shell

```bash
python manage.py shell
```

### Tests ausführen

```bash
python manage.py test
python manage.py test apps.core
```

### Admin Interface

```bash
# Superuser erstellen
python manage.py createsuperuser

# Admin: http://localhost:8000/admin/
```

## Umgebungsvariablen

Die `.env` Datei wird automatisch von Django geladen.

**Wichtige Variablen:**

- `SECRET_KEY` – Geheim halten!
- `DEBUG` – True in Development, False in Production
- `ALLOWED_HOSTS` – Domains, die Django servieren darf
- `ENVIRONMENT` – development, staging, production

Siehe [.env.example](./.env.example) für alle Optionen.

## Häufige Probleme

### Django startet nicht – ".env nicht gefunden"

```bash
cp .env.example .env
```

### Port 8000 bereits in Verwendung

```bash
python manage.py runserver 8001
```

### Migrations haben Fehler

```bash
python manage.py migrate --fake-initial
```

## Best Practices

✓ Virtual Environment immer aktivieren  
✓ `.env` nicht im Repository committen  
✓ Neue Dependencies zu `requirements.txt` hinzufügen  
✓ Migrations vor Commits durchführen  
✓ Tests lokal ausführen  
✓ Documentation aktualisieren  

## Ressourcen

- [Django Dokumentation](https://docs.djangoproject.com/)
- [django-environ Docs](https://django-environ.readthedocs.io/)
- Projekt-Dokumentation: [docs/](./docs/)

## Hilfe bekommen

Bei Fragen oder Problemen:
1. Schau in [docs/adr/](./docs/adr/) nach Architekturentscheidungen
2. Schau in [docs/standards/](./docs/standards/) nach Code-Konventionen
3. Starte den Development Server und teste
