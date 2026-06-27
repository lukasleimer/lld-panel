# LLD Panel UI Framework

## Übersicht

Das LLD Panel UI Framework ist ein **benutzerdefiniertes, leichtgewichtiges CSS-Framework** speziell für die Anforderungen einer klassischen Desktop-Verwaltungsanwendung.

## Projektphilosophie

### Warum ein eigenes Framework?

Bestehende Frameworks (Bootstrap, Tailwind, etc.) bringen folgende Probleme mit sich:

1. **Zu viel Overhead** – Für eine einfache Desktop-App sind hunderte von CSS-Klassen unnötig
2. **Moderne Designtrends** – Diese widersprechen der klassischen Desktop-Optik
3. **Abhängigkeitsverwaltung** – Externe Dependencies sind ein Wartungsproblem
4. **Konsistenz** – Die Kontrolle über alle Aspekte ist essential für eine einheitliche Optik
5. **Performance** – Ein maßgeschneidertes Framework ist deutlich kleiner

### Unsere Lösung

Ein **konsistentes, modernes Design mit klassischer Optik** – inspiriert von:

- Windows NT / Windows 95 Benutzeroberflächen
- Klassischen ERP-Systemen
- Zeitlosen Desktop-Anwendungen

### Kernprinzipien

1. **Funktionalität vor Ästhetik** – Die UI dient dem Workflow
2. **Konsistenz** – Alle Komponenten sehen einheitlich aus
3. **Klarheit** – Keine versteckten Funktionen oder verwirrenden Designs
4. **Effizienz** – Minimales CSS, maximale Wiederverwendung
5. **Wartbarkeit** – Strukturierter Code, klare Dokumentation
6. **Zugänglichkeit** – Semantisches HTML, klare Navigationswege
7. **Desktop First** – Keine Mobile-Optimierung erforderlich

## Architektur

### Ordnerstruktur

```
static/css/
├── panel.css              # Hauptdatei - importiert alle anderen
├── tokens.css             # Zentrale Design Tokens (Farben, Abstände, Typen)
├── reset.css              # Browser-Normalisierung
├── typography.css         # Schriften, Überschriften, Text
├── layout.css             # Globales Layout, Grid, Flexbox
└── components/
    ├── button.css         # Button-Komponente
    ├── form.css           # Formulare, Input, Select
    ├── table.css          # Tabellen
    ├── panel.css          # Container-Komponente
    └── toolbar.css        # Toolbar-Komponente
```

### Import-Reihenfolge

```css
/* panel.css */
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

**Begründung**: Tokens zuerst (Basis), dann Reset, dann Typo, dann Layout, dann Komponenten

## Design Tokens

Design Tokens sind zentrale **Designvariablen**, die garantieren, dass alle Komponenten eine einheitliche Optik haben.

### Kategorie: Farben

```css
--color-bg-primary: #c0c0c0;        /* Windows 95 Grau */
--color-bg-secondary: #dfdfdf;      /* Heller Grau */
--color-text-primary: #000000;      /* Schwarze Schrift */
--color-text-secondary: #666666;    /* Grau Schrift */
--color-header-bg: #000080;         /* Klassisches Dunkelblau */
--color-header-text: #ffffff;       /* Weiße Schrift */
```

### Kategorie: Abstände

```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 12px;
--spacing-lg: 16px;
--spacing-xl: 20px;
```

### Kategorie: Typografie

```css
--font-family: Segoe UI, Tahoma, Arial, sans-serif;
--font-size-base: 11px;
--font-size-sm: 10px;
--font-size-md: 12px;
--font-size-lg: 14px;
```

### Kategorie: Rahmen

```css
--border-width: 1px;
--border-width-thick: 2px;
--color-border-dark: #808080;
--color-border-light: #ffffff;
```

## CSS-Regel (Naming Convention)

### Allgemeine Klassen

Alle Klassen sind **funktionsorientiert**, nicht seitenbezogen:

```css
/* RICHTIG */
.button {}
.form-group {}
.table {}
.panel {}
.app-header {}

/* FALSCH */
.dashboard-button {}
.customer-form {}
.users-table {}
```

### Block-Element-Modifier (BEM) bei Bedarf

Bei komplexeren Komponenten können wir BEM-Notation verwenden:

```css
.panel {}
.panel__header {}
.panel__content {}
.panel__footer {}
```

### Utility-Klassen

Sparsam eingesetzte Utilities für gemeinsame Patterns:

```css
.text-center { text-align: center; }
.mb-md { margin-bottom: var(--spacing-md); }
.w-full { width: 100%; }
```

## Komponentenstrategie

### 1. Atomare Komponenten

Einfache, wiederverwendbare Bausteine:

- **Button** – Ein Klick-Element
- **Input** – Eingabefeld
- **Label** – Text-Label

### 2. Molekulare Komponenten

Kombinationen aus atomaren Komponenten:

- **Form Group** – Label + Input + Validation
- **Toolbar** – Button + Button + Divider

### 3. Organische Komponenten

Komplette UI-Abschnitte:

- **Panel** – Header + Content + Footer
- **Table** – Header + Rows + Footer
- **Navigation** – Links in einer Liste

## Ziele des Frameworks

1. ✓ **Minimalist** – Nur notwendiges CSS
2. ✓ **Konsistent** – Globale Design Tokens
3. ✓ **Wartbar** – Klare Struktur, gute Dokumentation
4. ✓ **Wiederverwendbar** – Komponenten für alle Seiten
5. ✓ **Keine Dependencies** – Reines CSS
6. ✓ **Desktop optimiert** – Für Admin-Tools designt
7. ✓ **Professionell** – Klassische, zeitlose Optik

## Implementierungsrichtlinien

- Alle neuen Komponenten in `components/` Ordner
- Design Tokens verwenden, nie Hardcoded Colors
- Keine Inline-Styles im HTML
- Semantisches HTML nutzen
- CSS nicht in Templates
- Komponenten sind Basis für alle Seiten

## Nächste Schritte

1. CSS-Struktur aufbauen (diese Architektur)
2. Design Tokens definieren (tokens.css)
3. Reset und Basis-Styles (reset.css, typography.css)
4. Layout-System (layout.css)
5. Komponenten umsetzen (components/*.css)
6. Komponenten-Templates erstellen (templates/components/*/)
7. Erste Seiten mit Komponenten aufbauen
