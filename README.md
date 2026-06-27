# LLD Panel

Internes Verwaltungsportal für **Lukas Leimer Development (LLD)**.

## Ziel

Das Panel dient als zentrale Verwaltungsplattform für:

- Kundenverwaltung
- Projekte
- Website-Templates
- Hosting
- Domains
- Deployments
- Monitoring
- Dokumentation

## Technologie

- Python 3.14
- Django 6.0
- PostgreSQL (später)
- Docker (später)

## Status

🚧 Sprint 4 – Release Foundation ✅

## Quick Start

### Erste Schritte

```bash
# 1. Virtual Environment
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows
source .venv/bin/activate           # macOS/Linux

# 2. Dependencies
pip install -r requirements/development.txt

# 3. Environment konfigurieren
cp .env.example .env

# 4. Server starten
cd src
python manage.py runserver
```

**Öffnen:** http://localhost:8000

### Dokumentation

- 📖 [Development Setup](DEVELOPMENT.md)
- 🏗️ [Architecture](docs/architecture/)
- 🔧 [Standards](docs/standards/)
- 📋 [ADRs](docs/adr/)
- 🚀 [Deployment](docs/deployment/)

### Requirements

Die Anforderungen sind nach Umgebung organisiert:

```
requirements/
├── base.txt              # Gemeinsam
├── development.txt       # Dev-Tools
└── production.txt        # Production
```

Siehe [requirements/README.md](requirements/README.md)

## Version

Aktuelle Version: `0.1.0-alpha.1`

Versionsnummer wird zentral verwaltet: [src/config/version.py](src/config/version.py)