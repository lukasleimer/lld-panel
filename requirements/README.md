# Requirements Management

Die Anforderungen sind jetzt modular organisiert:

## Installation

### Development (lokal)
```bash
pip install -r requirements/development.txt
```

### Production
```bash
pip install -r requirements/production.txt
```

### Basis (CI/CD, Testing)
```bash
pip install -r requirements/base.txt
```

## Struktur

- `requirements/base.txt` – Gemeinsame Abhängigkeiten
- `requirements/development.txt` – Dev-Tools + base
- `requirements/production.txt` – Production Packages + base

## Details

Siehe [docs/standards/dependencies.md](docs/standards/dependencies.md)
