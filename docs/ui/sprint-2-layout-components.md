# Sprint 2 – Layout-Komponenten

## Übersicht

Dieser Sprint implementiert die drei Haupt-Layout-Komponenten für das LLD Panel:

1. **Header** – Anwendungs-Kopfzeile mit Titel, Version, Benutzer
2. **Sidebar** – Feste Navigation mit 5 Hauptlinks
3. **Footer** – Statusleiste mit System-Informationen

## Architektur

### Komponenten-Struktur

```
templates/components/
├── header/
│   └── header.html          ← Kopfzeile
├── sidebar/
│   └── sidebar.html         ← Navigation
└── footer/
    └── footer.html          ← Statusleiste
```

### Integration in base.html

```html
<div class="container">
    {% include "components/header/header.html" %}
    
    <div class="main-wrapper">
        {% include "components/sidebar/sidebar.html" %}
        
        <main class="app-content">
            {% block content %}{% endblock %}
        </main>
    </div>
    
    {% include "components/footer/footer.html" %}
</div>
```

**Vorteil:** base.html bleibt sauber, Komponenten sind austauschbar

## Component: Header

### Zweck
Anwendungs-Kopfzeile mit Programm-Identität und Benutzer-Info

### Inhalte
- Programmtitel (links)
- Version (Platzhalter)
- Aktueller Benutzer (rechts, Platzhalter)

### Design
- Dunkelblaues Background (#000080)
- Weiße Schrift
- Fixe Höhe: 40px
- Keine Icons, Buttons, Suche

### CSS-Klassen
- `.app-header` – Container
- `.app-header h1` – Titel
- Utility: `.text-right` für Benutzer

## Component: Sidebar

### Zweck
Globale Navigation, immer sichtbar

### Inhalte
- Dashboard
- Kunden
- Projekte
- Templates
- Einstellungen

### Design
- Fixe Breite: 200px
- Hellgrauer Background (#c0c0c0)
- Klare Trennung zwischen Items
- Hover-Effekt bei Links
- Scrollbar wenn nötig

### CSS-Klassen
- `.app-nav` – Container
- `.app-nav ul` / `li` – Liste
- `.app-nav a` – Links mit Hover/Active

### Navigation-URLs

```
/ → Dashboard
/customers/ → Kunden
/projects/ → Projekte
/templates/ → Templates
/settings/ → Einstellungen
```

## Component: Footer

### Zweck
Statusleiste mit System-Informationen

### Inhalte
- Status: Ready
- Umgebung: Development
- Version: 0.1.0

### Design
- Fixe Höhe: 28px
- Hellgrauer Background (#c0c0c0)
- Schwarze Schrift
- Kleine Schrift: 10px
- Oben Trennlinie

### CSS-Klassen
- `.app-footer` – Container
- Utility: `.text-muted` für weniger wichtigen Text

## HTML-Standards (eingehalten)

✓ Semantisches HTML (`<header>`, `<nav>`, `<footer>`)
✓ Klare Hierarchie
✓ Keine Inline-Styles
✓ Konsistente Klasse-Namen
✓ Django-Template Syntax
✓ Keine Emojis

## CSS-Standards (eingehalten)

✓ Nur Variablen verwenden
✓ Keine Magic Numbers
✓ Klare BEM-Notation (optional)
✓ Layout.css definiert alle Styles
✓ Keine neuen CSS-Dateien nötig

## Reusability

Diese Komponenten sind:
- **Stateless** – Keine Django-Context-Logik nötig
- **Austauschbar** – Können einfach ersetzt werden
- **Erweiterbar** – `include` with `with` Variablen möglich
- **Konsistent** – Einheitliche Klasse-Namen

## Deployment

Nach diesem Sprint:
- ✓ Neue Seiten können base.html nutzen
- ✓ Design ist konsistent
- ✓ Komponenten sind getestet
- ✓ Dokumentation ist aktuell
