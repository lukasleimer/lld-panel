# Django Standards

## Projektstruktur

### Apps im `apps/` Ordner

```
src/
├── apps/
│   ├── core/          ← Zentrale Infrastruktur
│   ├── customers/     ← Kundenverwaltung (später)
│   ├── projects/      ← Projektmanagement (später)
│   └── __init__.py
├── config/
├── templates/
├── static/
└── manage.py
```

**Grund:** Klare Struktur, einfaches Import-System (`apps.core`, `apps.customers`)

## App-Struktur

### Minimale App

```
core/
├── migrations/
│   └── __init__.py
├── templates/
│   └── dashboard.html
├── __init__.py
├── admin.py
├── apps.py
├── context_processors.py
├── urls.py
└── views.py
```

**Nicht nötig (noch):**
- `models.py` – Wenn keine DB-Models
- `forms.py` – Wenn keine Forms
- `admin.py` – Wenn keine Admin-Interface
- `tests.py` – Wird später hinzugefügt

### Volle App (mit Models, Forms, Tests)

```
customers/
├── migrations/
├── templates/
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
└── views.py
```

## Views

### Function-Based Views (für einfache Views)

```python
from django.shortcuts import render

def dashboard(request):
    context = {'page_title': 'Dashboard'}
    return render(request, 'dashboard.html', context)
```

**Wann:** Einfache Anfragen, einfache Logik

### Class-Based Views (für komplexe Views)

```python
from django.views import View
from django.views.generic import ListView

class CustomerListView(ListView):
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'
```

**Wann:** CRUD-Operationen, komplexe Logik, DRY Code

## URLs

### url.py Pattern

```python
from django.urls import path
from . import views

app_name = 'core'  ← Namespace

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('health/', views.health_check, name='health_check'),
]
```

**Namespace:** Ermöglicht `{% url 'core:home' %}` im Template

### Zentrale url.py

```python
from django.urls import path, include

urlpatterns = [
    path('', include('apps.core.urls')),
    path('customers/', include('apps.customers.urls')),
    path('projects/', include('apps.projects.urls')),
]
```

## Context Processors

### Was ist ein Context Processor?

Eine Funktion, die Daten zu JEDEM Template hinzufügt:

```python
# apps/core/context_processors.py
from django.utils import timezone

def core_context(request):
    return {
        'app_name': 'LLD Panel',
        'app_version': '0.1.0',
        'current_user': request.user,
        'current_year': timezone.now().year,
    }
```

### In Template verwenden

```html
<footer>
    <span>{{ app_name }} v{{ app_version }}</span>
    <span>Logged in as: {{ current_user }}</span>
</footer>
```

### In settings.py registrieren

```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'apps.core.context_processors.core_context',  ← Hier
            ],
        },
    },
]
```

## Templates

### Verzeichnis-Struktur

```
templates/
├── base.html                      ← Basis-Template
├── dashboard.html                 ← Dashboard
├── 404.html                       ← Fehlerseite
├── 500.html                       ← Fehlerseite
└── components/                    ← Komponenten
    ├── header/
    ├── sidebar/
    └── footer/
```

### Template-Namen

**App-Template:** `core/dashboard.html`
- Ort: `apps/core/templates/core/dashboard.html`
- Grund: Namespace verhindert Konflikte

**Projekt-Template:** `dashboard.html`
- Ort: `templates/dashboard.html`
- Grund: Top-level, zentral

## Error Handling

### Handler registrieren

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

handler404 = 'apps.core.views.page_not_found'
handler500 = 'apps.core.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
]
```

### Error Views

```python
# apps/core/views.py
from django.shortcuts import render

def page_not_found(request, exception):
    return render(request, '404.html', status=404)

def server_error(request):
    return render(request, '500.html', status=500)
```

## Settings-Struktur

### Wichtige Einstellungen

```python
# Basis
DEBUG = True
ALLOWED_HOSTS = ['*']  # Development only!

# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'apps.core',  # ← Unsere App
]

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'src' / 'templates'],
        'APP_DIRS': True,  ← Sucht auch in app/templates/
    },
]

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'src' / 'static'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'src' / 'db.sqlite3',
    }
}
```

## Imports-Konvention

```python
# RICHTIG – Django imports zuerst
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

# Dann App-Imports
from apps.core.models import SomeModel
from .views import some_view

# FALSCH – Unsortierte Imports
from .views import some_view
from django.shortcuts import render
from apps.core.models import SomeModel
```

## One App Per Folder

```
apps/
├── __init__.py           ← Macht apps/ zu Package
├── core/
│   ├── __init__.py
│   ├── urls.py
│   ├── views.py
│   └── ...
├── customers/
│   ├── __init__.py
│   ├── urls.py
│   ├── views.py
│   └── ...
```

**apps/__init__.py ist leer:**
```python
# apps/__init__.py – Leer!
```

## Checkliste für neue App

- [ ] App erstellt mit `python manage.py startapp [name]`
- [ ] In `INSTALLED_APPS` registriert
- [ ] `urls.py` erstellt mit `app_name = 'xxx'`
- [ ] In zentrale `urls.py` mit `include()` eingebunden
- [ ] `views.py` mit Views implementiert
- [ ] `templates/[app]/` Ordner angelegt
- [ ] Tests geschrieben (`tests.py`)
- [ ] Dokumentation aktualisiert
