# ADR-0001: Eigenes UI Framework statt Bootstrap/Tailwind

**Status:** ANGENOMMEN  
**Datum:** 2026-06-27  
**Entscheidung:** Ein benutzerdefiniertes CSS-Framework für LLD Panel entwickeln

## Kontext

Das LLD Panel ist eine interne, **Desktop-basierte Verwaltungsanwendung**. Die traditionelle Herangehensweise wäre, ein bestehendes Framework wie Bootstrap oder Tailwind zu nutzen.

### Anforderungen

- Klassische Desktop-Anwendungsoptik (Windows 95 / ERP-Systeme)
- Maximale Kontrolle über das Design
- Minimale externe Dependencies
- Schnelle Performance
- Konsistente, wartbare Codebase

### Alternativen

| Option | Vorteile | Nachteile |
|--------|----------|-----------|
| **Bootstrap** | Weit verbreitet, viel Dokumentation | Zu schwer, moderne Optik, viel Overhead |
| **Tailwind** | Produktiv, viel Kontrolle | Komplexe Config, moderne Ästhetik |
| **Eigenes Framework** | Volle Kontrolle, Minimal, spezifisch | Mehr Wartung, weniger externe Docs |

## Entscheidung

**Wir entwickeln ein eigenes, leichtgewichtiges UI Framework** mit folgenden Charakteristika:

1. **Modulare Struktur** – Separate CSS-Dateien für Tokens, Reset, Typography, Layout, Komponenten
2. **Design Tokens** – Zentrale Variablen für Farben, Abstände, Typografie
3. **Komponentenorientiert** – Wiederverwendbare UI-Komponenten
4. **Keine Dependencies** – Reines CSS, kein JavaScript Framework
5. **Desktop First** – Für Admin-Apps optimiert, keine Mobile-Concerns
6. **Klassische Optik** – Windows 95 / klassische Benutzeroberflächen als Inspiration

## Rationale

### 1. Kontrolle über die Optik

Eigenes Framework garantiert, dass die Anwendung **genau so aussieht**, wie wir es designt haben. Bootstrap/Tailwind würden ihre eigene Design-Philosophie aufzwingen.

### 2. Performance

Ein benutzerdefiniertes Framework ist **deutlich kleiner** als allgemeine Frameworks:

```
Bootstrap:  ~180 KB (minified)
Tailwind:   ~100 KB (minified)
Unser Framework: ~15 KB (estimated)
```

### 3. Wartbarkeit

Mit einem kleinen, fokussierten Framework können wir:
- Schnell alle CSS-Dateien verstehen
- Änderungen schnell durchführen
- Keine unnötigen Klassen laden

### 4. Konsistenz

Ein zentral verwaltetes Framework garantiert, dass:
- Alle Button gleich aussehen
- Alle Formulare konsistent sind
- Alle Tabellen einheitlich formatiert sind

### 5. Keine externen Dependencies

- Kein NPM, kein Build-Prozess für CSS nötig
- Keine Version-Konflikte
- Keine Security-Updates für CSS-Framework

## Implikationen

### Positiv

✓ Komplette Kontrolle über das Design  
✓ Minimal-CSS, maximale Performance  
✓ Einfache Wartung und Änderungen  
✓ Leicht zu dokumentieren und zu lehren  
✓ Keine Abhängigkeiten  

### Negativ / Anforderungen

✗ Wir müssen das Framework selbst bauen und warten  
✗ Weniger externe Ressourcen online  
✗ Neuer Code = potenzielle Bugs  

**Mitigation:** Gute Dokumentation, Code Reviews, Tests

## Implementierungsplan

1. **Fase 1: Basis** – tokens.css, reset.css, typography.css, layout.css
2. **Fase 2: Komponenten** – button.css, form.css, table.css, panel.css, toolbar.css
3. **Fase 3: Templates** – HTML-Templates für jede Komponente
4. **Fase 4: Seiten** – Erste Seiten mit Komponenten aufbauen
5. **Fase 5: Dokumentation** – Architecture, Standards, Component Guide

## Erfolgs-Metriken

- [ ] CSS-Framework ist < 20 KB (minified)
- [ ] Alle Komponenten sind dokumentiert
- [ ] Komponenten-Wiederverwendung: > 80%
- [ ] Build Time für CSS: < 100ms
- [ ] 100% Browser-Kompatibilität (moderne Browser)

## Entscheidungs-Zeitpunkt

Diese Entscheidung wird getroffen **vor der ersten Seite** implementiert wird. Später zu ändern wäre sehr teuer.

## Nächste ADRs

- ADR-0002: Design Token System
- ADR-0003: CSS Naming Convention
- ADR-0004: Component Architecture
- ADR-0005: Responsive Design Policy (wird sein: Desktop Only)

## Gültig ab

27.06.2026

---

**Entscheidung getroffen von:** Entwicklerteam  
**Letzte Überprüfung:** 27.06.2026
