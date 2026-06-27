# HTML Standards

## Zweck

Dieses Dokument definiert die HTML-Konventionen für das LLD Panel Projekt. Alle HTML-Code muss diesen Standards entsprechen.

## Semantisches HTML

### Verwende semantische Elemente

```html
<!-- RICHTIG -->
<header>
    <h1>LLD Panel</h1>
</header>

<nav>
    <ul>
        <li><a href="/dashboard/">Dashboard</a></li>
    </ul>
</nav>

<main>
    <article>
        <h2>Artikel-Titel</h2>
        <p>Inhalt...</p>
    </article>
</main>

<footer>
    <p>Copyright 2026</p>
</footer>

<!-- FALSCH -->
<div class="header">
    <div class="title">LLD Panel</div>
</div>

<div class="navigation">
    <div><a href="/dashboard/">Dashboard</a></div>
</div>
```

### Richtige Element-Auswahl

| Zweck | Element | NICHT verwenden |
|-------|---------|-----------------|
| Kopfzeile | `<header>` | `<div class="header">` |
| Navigation | `<nav>` | `<div class="nav">` |
| Hauptinhalt | `<main>` | `<div class="main">` |
| Artikel/Beitrag | `<article>` | `<div class="article">` |
| Abschnitt | `<section>` | `<div class="section">` |
| Seitenleiste | `<aside>` | `<div class="sidebar">` |
| Fußzeile | `<footer>` | `<div class="footer">` |
| Überschrift | `<h1>`-`<h6>` | `<div class="heading">` |
| Liste | `<ul>` / `<ol>` / `<dl>` | `<div><span>...</span></div>` |
| Tabelle | `<table>` | `<div><div>...</div></div>` |

## Überschriften-Hierarchie

```html
<!-- RICHTIG -->
<h1>Seitentitel</h1>        <!-- Nur eine h1 pro Seite -->
<h2>Hauptabschnitt</h2>
<h3>Unterabschnitt</h3>

<!-- FALSCH -->
<h1>Seitentitel</h1>
<h1>Anderer Titel</h1>       <!-- Zwei h1 auf einer Seite -->

<h1>Titel</h1>
<h3>Unterabschnitt</h3>      <!-- Überspringe h2 -->
```

**Warum?** Assistive Technologien und Suchmaschinen verlassen sich auf die Hierarchie.

## Formulare

### Immer `<label>` verwenden

```html
<!-- RICHTIG -->
<div class="form-group">
    <label for="email">Email</label>
    <input type="email" id="email" name="email">
</div>

<!-- FALSCH -->
<div>
    Email:
    <input type="email">
</div>

<!-- AUCH FALSCH -->
<input type="email" placeholder="Email">
```

**Warum?** Labels verbessern Zugänglichkeit und Nutzbarkeit.

### Input-Typen verwenden

```html
<!-- RICHTIG -->
<input type="email" name="email">
<input type="password" name="password">
<input type="number" name="count">
<input type="date" name="birth_date">
<input type="checkbox" name="agree">
<input type="radio" name="choice">

<!-- FALSCH -->
<input type="text" name="email">  <!-- Sollte type="email" sein -->
```

### Fieldset für Gruppen

```html
<!-- RICHTIG -->
<fieldset>
    <legend>Anrede</legend>
    <label>
        <input type="radio" name="title" value="mr"> Herr
    </label>
    <label>
        <input type="radio" name="title" value="ms"> Frau
    </label>
</fieldset>

<!-- FALSCH -->
<div>
    <div><input type="radio" name="title"> Herr</div>
    <div><input type="radio" name="title"> Frau</div>
</div>
```

## Tabellen

```html
<!-- RICHTIG -->
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Max Mustermann</td>
            <td>max@example.com</td>
            <td>Aktiv</td>
        </tr>
    </tbody>
</table>

<!-- FALSCH -->
<div class="table">
    <div class="row">
        <div class="cell">Max Mustermann</div>
    </div>
</div>
```

## Django Templates

### Struktur

```html
{% extends "base.html" %}
{% load static %}

{% block title %}Seitentitel{% endblock %}

{% block content %}
    <h1>Seitentitel</h1>
    
    <div class="panel">
        <!-- Inhalt -->
    </div>
{% endblock %}
```

### Komponenten einbinden

```html
<!-- RICHTIG – Klare Syntax -->
{% include "components/button/button.html" %}
{% include "components/table/table.html" with rows=customers %}
{% include "components/form/form.html" with form=customer_form %}

<!-- FALSCH – Zu viel Logik im Template -->
{% if user.is_authenticated %}
    {% if user.is_staff %}
        ... komplexe Logik ...
    {% endif %}
{% endif %}
```

**Vorschlag:** Komplexe Logik in Views, nicht in Templates.

### Static Files

```html
<!-- RICHTIG -->
{% load static %}
<link rel="stylesheet" href="{% static 'css/panel.css' %}">
<img src="{% static 'img/logo.png' %}" alt="Logo">

<!-- FALSCH -->
<link rel="stylesheet" href="/static/css/panel.css">
<img src="/static/img/logo.png" alt="Logo">
```

## Attribute

### Immer Alt-Text für Bilder

```html
<!-- RICHTIG -->
<img src="{% static 'img/logo.png' %}" alt="LLD Panel Logo">

<!-- FALSCH -->
<img src="{% static 'img/logo.png' %}">
<img src="{% static 'img/logo.png' %}" alt="image">
```

### Title für wichtige Links

```html
<!-- RICHTIG -->
<a href="/customers/" title="Zur Kundenverwaltung">Kunden</a>

<!-- FALSCH -->
<a href="/customers/">Kunden</a>  <!-- Optional, aber empfohlen -->
```

### Data-Attribute für JavaScript

```html
<!-- Wenn JavaScript nötig ist -->
<button class="button" data-action="delete" data-id="123">
    Löschen
</button>

<!-- JavaScript -->
<script>
    document.querySelector('[data-action="delete"]').addEventListener('click', (e) => {
        const id = e.target.dataset.id;
        // Aktion...
    });
</script>
```

## CSS-Klassen im HTML

### Konsistente Klasse-Namen

```html
<!-- RICHTIG -->
<button class="button">Speichern</button>
<button class="button button--primary">Hinzufügen</button>

<div class="panel">
    <div class="panel__header">
        <h2>Titel</h2>
    </div>
    <div class="panel__content">
        Inhalt...
    </div>
</div>

<!-- FALSCH -->
<button class="btn">Speichern</button>              <!-- Inkonsistent -->
<button class="save-button">Speichern</button>     <!-- Page-spezifisch -->
<button style="background-color: blue;">...</button> <!-- Inline-Style -->
```

### Keine Inline-Styles

```html
<!-- RICHTIG – Keine Styles im HTML -->
<div class="panel">
    Inhalt...
</div>

<!-- FALSCH – Inline-Styles -->
<div style="padding: 12px; background-color: #c0c0c0;">
    Inhalt...
</div>
```

## Attribute-Reihenfolge

```html
<!-- Empfohlene Reihenfolge -->
<input
    type="email"
    id="email"
    name="email"
    class="form-control"
    placeholder="max@example.com"
    required
    aria-label="Email-Adresse"
>
```

**Reihenfolge:**
1. `type`, `name`, `id`
2. `class`
3. Validierung (`required`, `pattern`, etc.)
4. Accessibility (`aria-*`, `title`)
5. Data (`data-*`)

## Struktur-Template

```html
{% extends "base.html" %}
{% load static %}

{% block title %}Seite - LLD Panel{% endblock %}

{% block content %}
    <!-- Kopfzeile -->
    <header class="page-header">
        <h1>Seitentitel</h1>
    </header>

    <!-- Toolbar/Aktionen -->
    <div class="toolbar">
        <button class="button">Neu</button>
        <button class="button">Bearbeiten</button>
    </div>

    <!-- Hauptinhalt -->
    <main>
        <div class="panel">
            <div class="panel__header">
                <h2>Panel-Titel</h2>
            </div>
            <div class="panel__content">
                <!-- Inhalt -->
            </div>
        </div>
    </main>
{% endblock %}
```

## Keine Emojis

```html
<!-- FALSCH -->
<h1>Dashboard 📊</h1>
<button>Speichern ✓</button>

<!-- RICHTIG -->
<h1>Dashboard</h1>
<button>Speichern</button>
```

## Checkliste für neues HTML

- [ ] Semantische Elemente (`<header>`, `<nav>`, `<main>`, `<footer>`)
- [ ] Korrekte Überschriften-Hierarchie (h1, h2, h3, ...)
- [ ] `<label>` für alle Form-Inputs
- [ ] `alt`-Texte für Bilder
- [ ] Keine Inline-Styles
- [ ] Keine Page-spezifischen CSS-Klassen
- [ ] Konsistente Klasse-Namen
- [ ] Django Static File Syntax
- [ ] Keine Emojis
- [ ] Gut strukturiert und lesbar
- [ ] ARIA-Attribute bei Bedarf

## Ressourcen

- [HTML Living Standard](https://html.spec.whatwg.org/)
- [MDN HTML Guide](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [Web Content Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Django Template Documentation](https://docs.djangoproject.com/en/stable/topics/templates/)
