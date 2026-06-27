# Version Management

## Centralized Version

Die Versionsnummer ist **an einer Stelle** definiert:

```python
# src/config/version.py
VERSION = "0.1.0-alpha.1"
```

**Alle anderen Module importieren von dort:**

```python
from config.version import VERSION
```

## Wo wird die Version verwendet?

### 1. UI Components (Header, Footer)

**Vorher:**
```html
<!-- header.html -->
<span>Version 0.1.0</span>  <!-- Hart codiert ❌ -->
```

**Nachher:**
```html
<!-- header.html -->
<span>Version {{ app_version }}</span>  <!-- Aus Context ✓ -->
```

Context kommt aus Context Processor (siehe unten).

### 2. Context Processor (Template-Context)

**Vorher:**
```python
# context_processors.py
'app_version': '0.1.0',  # Hart codiert ❌
```

**Nachher:**
```python
# context_processors.py
from config.version import VERSION

'app_version': VERSION,  # Aus version.py ✓
```

### 3. API Response (health_check)

**Zukünftig:**
```python
# views.py
from config.version import VERSION

def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'version': VERSION,  # Aus version.py ✓
    })
```

### 4. Management Commands

```python
# commands/version.py
from config.version import VERSION

def handle(self, *args, **options):
    self.stdout.write(f"LLD Panel Version: {VERSION}")
```

### 5. Package Metadata (zukünftig)

```python
# setup.py
from src.config.version import VERSION

setup(
    name='lld-panel',
    version=VERSION,  # Aus version.py ✓
)
```

## Versionierungsschema

```
MAJOR.MINOR.PATCH-PRERELEASE.NUMBER

0.1.0-alpha.1  = Pre-Release, Features noch in Entwicklung
0.1.0-beta.1   = Beta Testing, Features abgeschlossen
0.1.0-rc.1     = Release Candidate, nur Bugfixes
0.1.0          = Stable Release ✓
0.2.0          = Neues Minor Release (neue Features)
1.0.0          = Major Release (Breaking Changes)
```

## Release Workflow

### Alpha → Beta

```bash
# Nur eine Datei ändern:
vim src/config/version.py
# VERSION = "0.1.0-alpha.1" → "0.1.0-beta.1"

# Commit & Push
git add .
git commit -m "Release 0.1.0-beta.1"
git tag 0.1.0-beta.1

# Alles andere aktualisiert sich automatisch:
# - UI (Version 0.1.0-beta.1)
# - API Response (version: "0.1.0-beta.1")
# - Package Metadata (version='0.1.0-beta.1')
```

### Beta → Stable

```bash
vim src/config/version.py
# VERSION = "0.1.0-beta.1" → "0.1.0"

git add .
git commit -m "Release 0.1.0 - Stable"
git tag 0.1.0
```

### Micro-Release (Bugfix)

```bash
vim src/config/version.py
# VERSION = "0.1.0" → "0.1.1"

git add .
git commit -m "Release 0.1.1 - Bugfixes"
git tag 0.1.1
```

## Automation (CI/CD)

```yaml
# .github/workflows/release.yml
on:
  push:
    tags:
      - '[0-9]+.[0-9]+.[0-9]*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check version match
        run: |
          VERSION=$(grep "VERSION = " src/config/version.py | cut -d'"' -f2)
          TAG=${{ github.ref_name }}
          if [ "$VERSION" != "$TAG" ]; then
            echo "Version mismatch! $VERSION != $TAG"
            exit 1
          fi
      
      - name: Build & Deploy
        run: ./scripts/deploy.sh
```

## Best Practices

✓ Immer aus `src/config/version.py` importieren  
✓ Nie direkt in Templates hart codieren  
✓ Release-Schritte dokumentieren  
✓ Version-Tags mit Git erstellen  
✓ Versionsnummer in Commit-Message erwähnen  
✓ CHANGELOG aktualisieren  

## Siehe auch

- [ADR-0005: Centralized Version Management](../adr/0005-centralized-version-management.md)
- [Release Process](./release-process.md) (zukünftig)
