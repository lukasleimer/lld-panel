# CSS Standards

## Zweck

Dieses Dokument definiert die CSS-Konventionen für das LLD Panel Projekt. Alle CSS-Code muss diesen Standards entsprechen.

## Dateistruktur

### Haupt-Einstiegsdatei: `panel.css`

```css
/* panel.css - Importiert alle CSS-Module */
@import url('tokens.css');
@import url('reset.css');
@import url('typography.css');
@import url('layout.css');
@import url('components/button.css');
@import url('components/form.css');
@import url('components/table.css');
@import url('components/panel.css');
@import url('components/toolbar.css');
```

**Warum?** Ein zentraler Entry Point macht Abhängigkeiten klar und vereinfacht die Wartung.

### Module

#### `tokens.css`

Definiert alle **Design Tokens** als CSS-Variablen:

- Farben (primary, secondary, text, borders)
- Abstände (xs, sm, md, lg, xl)
- Typografie (Font-Familie, Größen)
- Rahmen (Breiten, Farben)
- Höhen/Breiten (Header, Navigation)

**Vorteile:**
- Single Source of Truth für Designwerte
- Einfache globale Änderungen
- Konsistente Werte überall

#### `reset.css`

Browser-Normalisierung:

- CSS Reset (margin, padding auf 0)
- Box-sizing: border-box
- Standardtypen für HTML-Elemente

**Warum?** Jeder Browser hat Default-Styles. Wir setzen eine einheitliche Basis.

#### `typography.css`

Schrift und Text:

- Font-Familie
- Font-Größen
- Überschriften (h1-h6)
- Absätze
- Links

**Warum separat?** Typografie ist ein eigenständiges System, das andere Komponenten nicht kennen müssen.

#### `layout.css`

Globales Layouts-System:

- Flex-Container (`display: flex`)
- Grid-Basis
- Margin/Padding Utilities
- Responsive Klassen (falls nötig)

**Warum?** Dieses System wird überall verwendet (Header, Navigation, Content).

#### `components/*.css`

Jede Komponente hat eine eigene CSS-Datei:

- `button.css` – Button-Styles
- `form.css` – Input, Textarea, Select
- `table.css` – Table, Th, Td
- `panel.css` – Container-Komponente
- `toolbar.css` – Toolbar/Action Bar

## Naming Convention

### Klasse-Namen

**Format:** `.[component]-[element]` oder `.[component]`

```css
/* Komponente */
.button {}

/* Element einer Komponente (BEM-Notation) */
.button__icon {}
.button__text {}

/* Modifier */
.button--primary {}
.button--disabled {}
```

### Keine Seiten-Klassen

```css
/* RICHTIG */
.table {}

/* FALSCH */
.customers-table {}
.dashboard-table {}
```

Stattdessen: Gleiche Komponenten-Klasse überall, nur HTML-Kontext ändert sich.

### Utility-Klassen

Minimale Utilities für häufige Patterns:

```css
.text-center {}
.text-right {}
.m-0 { margin: 0; }
.mb-lg { margin-bottom: var(--spacing-lg); }
.w-full { width: 100%; }
```

## CSS-Regeln

### 1. Variablen verwenden

```css
/* RICHTIG */
color: var(--color-text-primary);
margin: var(--spacing-md);

/* FALSCH */
color: #000000;
margin: 12px;
```

**Warum?** Globale Änderungen sind unmöglich ohne Variablen.

### 2. Keine Inline-Styles im HTML

```html
<!-- RICHTIG -->
<button class="button">Speichern</button>

<!-- FALSCH -->
<button style="background-color: red;">Speichern</button>
```

**Warum?** Inline-Styles sind nicht wartbar, schwer zu ändern, vermischen Struktur und Stil.

### 3. Strukturelle CSS-Eigenschaften

Verwende CSS nur für Layout, Abstände, Farben, Typografie – nicht für Behavior:

```css
/* RICHTIG – Struktur */
.button {
    padding: var(--spacing-sm) var(--spacing-lg);
    background-color: var(--color-button-face);
    border: var(--border-width-thick) solid;
}

/* FALSCH – Behavior im CSS */
.button {
    cursor: pointer;  /* Das gehört ins HTML (button-Element) */
    transition: all 0.3s ease;  /* Wir verwenden keine Animationen */
}
```

### 4. Keine Hardcoded Farben

```css
/* RICHTIG */
color: var(--color-text-primary);

/* FALSCH */
color: #000000;
color: #c0c0c0;
```

### 5. Keine Magic Numbers

```css
/* RICHTIG */
padding: var(--spacing-md);
margin-bottom: var(--spacing-lg);

/* FALSCH */
padding: 12px;
margin-bottom: 16px;
```

### 6. Keine Animationen

Klassische Desktop-Apps haben keine Animationen.

```css
/* FALSCH */
transition: all 0.3s ease;
animation: fadeIn 0.5s;

/* RICHTIG */
/* Keine Animationen */
```

### 7. Keine Schatten oder Farbverläufe

```css
/* FALSCH */
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
background: linear-gradient(to right, #c0c0c0, #dfdfdf);

/* RICHTIG */
/* Flach, einfach, klassisch */
border: var(--border-width-thick) solid var(--color-border-dark);
background-color: var(--color-bg-primary);
```

## Selektoren

### Spezifität minimieren

```css
/* RICHTIG – Niedrige Spezifität */
.button { }

/* OK – Klasse + Element */
.button button { }

/* FALSCH – Zu spezifisch */
#content .container .button { }
```

### Verschachtelung vermeiden

CSS sollte flach sein:

```css
/* RICHTIG */
.button { }
.button:hover { }
.button:active { }

/* NICHT empfohlen */
.button {
  .icon { }
  &:hover { }
}
```

(Wir verwenden keine CSS-Präprozessoren wie SCSS)

## Kommentare

Nutze Kommentare nur, wenn echten Mehrwert:

```css
/* RICHTIG – Erklärt warum */
.button {
    /* 3D-Effekt: heller Rahmen oben/links, dunkler unten/rechts */
    border-color: var(--color-button-highlight) var(--color-button-shadow) 
                  var(--color-button-shadow) var(--color-button-highlight);
}

/* FALSCH – Offensichtlich */
.button {
    /* Padding setzen */
    padding: var(--spacing-sm);
}
```

### Abschnitts-Kommentare

Unterteile CSS-Dateien in Abschnitte:

```css
/* ============================================================================
   BUTTONS
   ============================================================================ */

.button { }
.button:hover { }

/* ============================================================================
   FORMS
   ============================================================================ */

input { }
select { }
```

## Weitere Standards

### 1. Mobile-First ist NICHT nötig

Dieses Projekt ist Desktop-Only. Keine Media Queries für mobile Geräte.

### 2. Cross-Browser Kompatibilität

Moderne Browser (Chrome, Firefox, Safari, Edge). Keine IE11-Unterstützung nötig.

### 3. Performance

- Minimale Dateigrößen
- Keine unnötigen Deklarationen
- Keine redundanten Styles

### 4. Hierarchie

```
Tokens (Variablen)
    ↓
Reset (Normalisierung)
    ↓
Typography (Schriften)
    ↓
Layout (Flexbox, Grid)
    ↓
Components (Komplexe UI)
```

Komponenten bauen auf diesen Schichten auf, nicht andersherum.

## Checkliste für neue CSS

- [ ] Verwendet Design Tokens (Variablen)
- [ ] Keine Inline-Styles im HTML
- [ ] Keine Hardcoded Farben oder Abstände
- [ ] Keine Animationen
- [ ] Keine Schatten oder Farbverläufe
- [ ] Semantische HTML-Elemente
- [ ] Klare Klasse-Namen
- [ ] Dokumentiert (wenn komplex)
- [ ] Im richtigen CSS-Modul (komponenten/* oder basis)
- [ ] Keine Magic Numbers

## Hilfreiche Ressourcen

- [Mozilla CSS Guide](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [MDN Best Practices](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Cascade_and_inheritance)
- [Design Systems 101](https://www.nngroup.com/articles/design-systems-101/)
