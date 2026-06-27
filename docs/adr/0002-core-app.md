# ADR-0002: Core App Architektur

**Status:** ANGENOMMEN  
**Datum:** 2026-06-27  
**Entscheidung:** Eine dedizierte `core` App für Infrastruktur und globale Funktionen

## Kontext

Das LLD Panel wird mehrere Django-Apps haben:
- `core` – Infrastruktur
- `customers` – Kundenverwaltung
- `projects` – Projektmanagement
- `accounts` – Authentifizierung
- Weitere...

Die Frage ist: **Wo gehört die allgemeine Infrastruktur hin?**

### Alternativen

| Lösung | Vorteile | Nachteile |
|--------|----------|-----------|
| **Eigene `core` App** | Klar strukturiert, wiederverwendbar | Zusätzliche Komplexität |
| Alles in `config/` | Einfach | Keine Trennung, schwer zu testen |
| In jeder App redundant | Dezentralisiert | Duplicate Code, Wartungsproblem |

## Entscheidung

**Wir erstellen eine dedizierte `core` App** mit folgenden Charakteristika:

### Verantwortlichkeiten der Core App

✓ Dashboard / Home View  
✓ Health Check Endpoint  
✓ Globale Context Processor  
✓ Error Handling (404, 500)  
✓ Allgemeine URL-Struktur  

### Was Core NICHT enthält

✗ Business-Logik (Customer, Project, etc.)  
✗ Authentifizierung (separate `accounts` App)  
✗ Datenbank-Models (außer wenn absolut nötig)  
✗ Seiten-spezifische Logik  

## Rationale

### 1. Klare Separation of Concerns

Infrastruktur ≠ Business-Logik

```
core/               ← Framework, Infrastruktur
├── views.py
├── context_processors.py
└── urls.py

customers/          ← Business-Logik
├── models.py
├── forms.py
└── views.py
```

### 2. Wiederverwendbarkeit

Code in `core` kann in anderen Django-Projekten wiedergenutzt werden:

```python
# core/context_processors.py
def app_context(request):
    return {
        'app_version': '0.1.0',
        'environment': 'Development',
    }
```

Kann in jedem Projekt kopiert werden.

### 3. Testbarkeit

Core-Tests sind unabhängig von Business-Logik:

```python
def test_health_check():
    response = client.get('/health/')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'
```

### 4. Wartbarkeit

Änderungen an Core beeinflussen nicht Customers, Projects, etc.

Dashboard muss nicht angepasst werden, wenn Customers-Logik ändert.

### 5. Vorbereitung auf wachsende Komplexität

Später möchten wir vielleicht:
- Audit Logging
- Permission System
- Rate Limiting
- Caching Layer

Alles gehört in `core` ohne Business-Apps zu beeinflussen.

## Struktur

```
src/apps/core/
├── migrations/
├── templates/
│   └── dashboard.html
├── __init__.py
├── admin.py
├── apps.py
├── context_processors.py    ← Globale Context
├── urls.py
└── views.py
    ├── dashboard           ← Home Page
    ├── health_check        ← Health Monitor
    ├── page_not_found      ← 404 Handler
    └── server_error        ← 500 Handler
```

## Registrierung

### settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
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

### config/urls.py

```python
handler404 = 'apps.core.views.page_not_found'
handler500 = 'apps.core.views.server_error'

urlpatterns = [
    path('', include('apps.core.urls')),
    # path('customers/', include('apps.customers.urls')),  # Später
]
```

## Views

### Home View

```python
def dashboard(request):
    context = {'page_title': 'Dashboard'}
    return render(request, 'core/dashboard.html', context)
```

**URL:** `/`

### Health Check

```python
def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'version': '0.1.0',
        'timestamp': timezone.now().isoformat(),
    })
```

**URL:** `/health/`  
**Nutzen:** Deployment-Monitoring, Load Balancer

### Error Handler

```python
def page_not_found(request, exception):
    return render(request, '404.html', status=404)

def server_error(request):
    return render(request, '500.html', status=500)
```

## Context Processor

Macht Daten überall verfügbar:

```python
def core_context(request):
    return {
        'app_name': 'LLD Panel',
        'app_version': '0.1.0',
        'environment': 'Development',
    }
```

Im Template:
```html
<footer>
    <span>{{ app_name }} v{{ app_version }}</span>
    <span class="text-muted">{{ environment }}</span>
</footer>
```

## Grenzen der Core App

**Core ist bewusst klein und fokussiert.**

Das ist absichtlich.

### Was auch NICHT in Core gehört

- **Kundenverwaltung** → `customers`
- **Projektmanagement** → `projects`
- **Benutzer-Auth** → `accounts`
- **Reporting** → `reports`
- **Reports** → `reports`

Jede Geschäftsfunktion = neue App

## Erweiterbarkeit

Zukünftig können wir hinzufügen:

```python
# apps/core/decorators.py
def login_required_or_redirect(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper
```

Oder:

```python
# apps/core/middleware.py
class AuditLogMiddleware:
    def __call__(self, request):
        # Log all requests
        pass
```

Aber Core bleibt **Infrastructure First**, nie Business Logic.

## Best Practice Checklist

✓ Core enthält nur Infrastruktur  
✓ Error Handler sind zentral  
✓ Context Processor für globale Daten  
✓ Klare URL-Struktur  
✓ Separate App-Namespaces  
✓ Templates im app/templates/ Ordner  
✓ Keine Models (noch nicht)  
✓ Keine Business-Logik  

## Gültig ab

27.06.2026

---

**Entscheidung getroffen von:** Entwicklerteam  
**Nächste Überprüfung:** Nach Sprint 4 (customers App)
