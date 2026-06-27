# Core App

## Zweck

Die `core` App ist die technische Grundlage des LLD Panels. Sie enthält **ausschließlich Infrastruktur und keine Business-Logik**.

## Dateien

### `views.py`
Zentrale Views:
- `dashboard()` – Hauptseite/Dashboard (URL: `/`)
- `health_check()` – Health Monitor (URL: `/health/`)
- `page_not_found()` – 404 Error Handler
- `server_error()` – 500 Error Handler

### `urls.py`
URL-Routing:
```python
path('', views.dashboard, name='home')        # /
path('health/', views.health_check, name='health_check')  # /health/
```

### `context_processors.py`
Globale Template-Context:
- `app_name` – "LLD Panel"
- `app_version` – "0.1.0"
- `environment` – "Development"
- `current_user` – Aktueller Benutzer
- `current_year` – Aktuelles Jahr

### `templates/core/dashboard.html`
Dashboard-Startseite

### `models.py`
Leer – Keine DB-Models in Core

### `tests.py`
Tests für Core Views und Context Processor

## Verwendung

### In anderen Templates

```html
<!-- Globale Context verfügbar -->
<footer>
    <span>{{ app_name }} v{{ app_version }}</span>
    <span class="text-muted">{{ environment }}</span>
</footer>
```

### In Views

```python
from apps.core.views import dashboard

# Views sind automatisch in URLs verfügbar
```

## Konfiguration (in settings.py)

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

## Konfiguration (in urls.py)

```python
handler404 = 'apps.core.views.page_not_found'
handler500 = 'apps.core.views.server_error'

urlpatterns = [
    path('', include('apps.core.urls')),
]
```

## Nicht enthalten

✗ Customer, Project, oder andere Business-Models  
✗ Authentifizierung (gehört zu `accounts` App)  
✗ Reporting, Analytics, oder komplexe Logik  
✗ Seiten-spezifische Views

## Zukünftige Erweiterungen

Später können wir hinzufügen:
- Audit Logging (globale Middleware)
- Permission System
- Rate Limiting
- Caching Layer
- API Versioning

Aber Core bleibt **Infrastructure First**.

## Design-Prinzipien

✓ Eine Verantwortung pro Modul  
✓ Keine Business-Logik  
✓ Wiederverwendbar in anderen Projekten  
✓ Django Best Practices  
✓ Ausbaubar ohne Breaking Changes  
