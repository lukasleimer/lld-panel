# Django App Architecture

## Warum eine strukturierte App-Architektur?

Das LLD Panel besteht aus mehreren Django-Apps mit klaren Grenzen und Verantwortlichkeiten.

Jede App hat einen **Single Purpose** – eine klare Aufgabe, die sie erfüllt.

## App-Kategorien

### 1. Core App (Technische Grundlage)

**Zweck:** Zentrale, anwendungsübergreifende Infrastruktur

**Verantwortlichkeiten:**
- Home/Dashboard View
- Health Checks
- Globale Context Processor
- Error Handling (404, 500, etc.)
- Allgemeine Utilities (falls vorhanden)

**Was NICHT in Core:**
- Business-Logik
- Kundenmanagement
- Projektmanagement
- Authentifizierung (später: separate `accounts` App)

**Dateien:**
```
core/
├── migrations/
├── templates/
│   └── dashboard.html
├── __init__.py
├── admin.py
├── apps.py
├── urls.py
├── views.py
└── context_processors.py
```

### 2. Business Apps (Später)

**customers** – Kundenverwaltung
```
customers/
├── models.py      ← Customer, Contact
├── views.py       ← CRUD Views
├── urls.py
├── templates/
└── ...
```

**projects** – Projektmanagement
**templates** – Vorlagen
**accounts** – Benutzer & Authentifizierung

## URL-Struktur

```
/                          → Dashboard (core)
/health/                   → Health Check (core)

/customers/                → Liste (später)
/customers/<id>/           → Detail (später)

/projects/                 → Liste (später)
/projects/<id>/            → Detail (später)

/templates/                → Liste (später)
/settings/                 → Einstellungen (später)

/404                       → Error Page (core)
/500                       → Error Page (core)
```

## Context Processor

Die `context_processor.py` macht Daten überall verfügbar:

```python
def core_context(request):
    return {
        'app_name': 'LLD Panel',
        'app_version': '0.1.0',
        'environment': 'Development',
        'current_year': timezone.now().year,
    }
```

Im Template:
```html
<span>{{ app_name }} v{{ app_version }}</span>
<span class="text-muted">{{ environment }}</span>
```

## Views

### Home View

```python
def home(request):
    context = {
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard.html', context)
```

### Health Check View

```python
def health_check(request):
    data = {
        'status': 'ok',
        'timestamp': timezone.now().isoformat(),
        'version': '0.1.0',
    }
    return JsonResponse(data)
```

Nutzen: Deployment-Monitoring, Load-Balancer Health Checks

### Error Views

Django handle errors automatisch über:
- `handler404` in `urls.py`
- `handler500` in `urls.py`

Templates:
- `404.html`
- `500.html`

## Templates

### dashboard.html

```html
{% extends "base.html" %}

{% block title %}Dashboard - LLD Panel{% endblock %}

{% block content %}
    <h1>Dashboard</h1>
    <p>Willkommen zurück.</p>
{% endblock %}
```

### 404.html, 500.html

Einfache Error Pages (später implementiert)

## Konfiguration

### settings.py

```python
INSTALLED_APPS = [
    # Django standard apps
    'django.contrib.admin',
    'django.contrib.auth',
    # ...
    
    # LLD Panel Apps
    'apps.core',
    # 'apps.customers',  # Später
    # 'apps.projects',   # Später
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'src' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Standard
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # Custom
                'apps.core.context_processors.core_context',
            ],
        },
    },
]
```

### urls.py

```python
from django.contrib import admin
from django.urls import path, include

# Error Handlers
handler404 = 'apps.core.views.page_not_found'
handler500 = 'apps.core.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core URLs
    path('', include('apps.core.urls')),
    
    # Business URLs (später)
    # path('customers/', include('apps.customers.urls')),
    # path('projects/', include('apps.projects.urls')),
]
```

## Best Practices eingehalten

✓ **Apps sind modular** – Eine Verantwortung pro App
✓ **Klare Grenzen** – Core trennt Infrastruktur von Business-Logik
✓ **Wiederverwendbar** – Context Processor nutzen alle Templates
✓ **Framework-First** – Django Conventions befolgt
✓ **Fehlerbehandlung** – 404/500 Handler sind eingebunden

## Warum keine Business-Logik in Core?

1. **Wartbarkeit** – Core ändert sich selten, Business-Logik oft
2. **Testing** – Einfach zu testen, da keine komplexe Logik
3. **Reusability** – Core kann in anderen Projekten genutzt werden
4. **Skalierbarkeit** – Neue Apps hängen an Core an, verändern es nicht

## Zukünftige Erweiterungen

```
Sprint 4: customers App
Sprint 5: projects App
Sprint 6: accounts App (Authentifizierung)
Sprint 7: reports App
```

Jede App folgt demselben Muster wie `core`.
