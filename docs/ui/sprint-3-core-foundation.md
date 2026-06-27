# Sprint 3 – Core Foundation

## Übersicht

Sprint 3 implementiert die technische Grundlage des LLD Panels: die `core` Django-App.

Diese App enthält **ausschließlich Infrastruktur**, keine Business-Logik.

## Architektur

### App-Struktur

```
apps/
├── __init__.py
└── core/
    ├── migrations/
    ├── templates/core/
    │   └── dashboard.html
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── context_processors.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    └── README.md
```

### Views

#### dashboard (home)
- URL: `/`
- Template: `core/dashboard.html`
- Zweck: Hauptseite des Panels
- Daten: `page_title`

#### health_check
- URL: `/health/`
- Content-Type: `application/json`
- Response: `{ "status": "ok", "version": "0.1.0", ... }`
- Zweck: Deployment-Monitoring

#### page_not_found (404)
- Handler für nicht-existierende Seiten
- Template: `404.html`

#### server_error (500)
- Handler für Server-Fehler
- Template: `500.html`

### Context Processor

```python
def core_context(request):
    return {
        'app_name': 'LLD Panel',
        'app_version': '0.1.0',
        'environment': 'Development',
        'current_user': request.user,
        'current_year': timezone.now().year,
    }
```

**Verfügbar in jedem Template automatisch.**

### URL-Struktur

```
/                 → Dashboard (core:home)
/health/          → Health Check (core:health_check)
/admin/           → Django Admin
```

## Konfiguration

### settings.py

```python
INSTALLED_APPS = [
    # ...
    'apps.core',
]

TEMPLATES = {
    'OPTIONS': {
        'context_processors': [
            # ...
            'apps.core.context_processors.core_context',
        ],
    },
}
```

### urls.py

```python
handler404 = 'apps.core.views.page_not_found'
handler500 = 'apps.core.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
]
```

## Dateien geändert

### Neue Dateien

1. `apps/__init__.py` – Package marker
2. `apps/core/` komplette App
   - `__init__.py`
   - `admin.py`
   - `apps.py`
   - `context_processors.py`
   - `models.py`
   - `tests.py`
   - `urls.py`
   - `views.py`
   - `README.md`
   - `migrations/__init__.py`
   - `templates/core/dashboard.html`

3. `src/config/settings.py` – `apps.core` hinzugefügt, context processor registriert
4. `src/config/urls.py` – Error handler, core URLs include
5. `templates/404.html` – Error page
6. `templates/500.html` – Error page

### Dokumentation (neu)

7. `docs/architecture/django-apps.md` – Django App-Architektur
8. `docs/standards/django.md` – Django Konventionen
9. `docs/adr/0002-core-app.md` – Architekturentscheidung

## Standards eingehalten

### ADR-0001: Eigenes UI Framework
✓ Desktop-optimiert  
✓ Klassische Optik  
✓ Keine Bootstrap/Tailwind  

### ADR-0002: Core App Architektur
✓ Infrastruktur ≠ Business-Logik  
✓ Wiederverwendbar  
✓ Klare Grenzen  
✓ Testbar  

### Django Best Practices
✓ App-Struktur (`apps.core`)  
✓ URL Namespaces (`app_name = 'core'`)  
✓ Context Processor  
✓ Error Handler  
✓ Tests  

### CSS/HTML Standards
✓ Semantisches HTML  
✓ Base-Template Nutzung  
✓ Keine Inline-Styles  

## Tests

`apps/core/tests.py` enthält Tests für:
- Health Check Status Code
- Health Check JSON Response
- Dashboard Status Code
- Dashboard Template
- Dashboard Context
- Core Context Processor

Ausführen:
```bash
python manage.py test apps.core
```

## Nächster Sprint

### Sprint 4: Customers App

Erste Business-App mit:
- Models (Customer, Contact)
- Views (CRUD)
- Forms
- Templates
- Admin Interface

Folgt demselben Muster wie `core`, aber mit Models und Business-Logik.

## Principles

✓ **Framework First** – Django Conventions, nicht Hacks  
✓ **Components before Modules** – Größere Apps später  
✓ **No Technical Debt** – Sauberer, wartbarer Code  
✓ **Single Responsibility** – Eine Aufgabe pro Modul  
✓ **Reusability First** – Core können andere Projekte nutzen  
