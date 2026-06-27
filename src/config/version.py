"""
Centralized Version Management for LLD Panel.

This is the SINGLE SOURCE OF TRUTH for version numbering.
All other modules should import from here.

See: docs/adr/0005-centralized-version-management.md
     docs/standards/version-management.md

Versioning Scheme:
- MAJOR.MINOR.PATCH-PRERELEASE.NUMBER
- 0.1.0-alpha.1 = Pre-Release
- 0.1.0-beta.1 = Beta Testing
- 0.1.0-rc.1 = Release Candidate
- 0.1.0 = Stable Release
"""

__version__ = "0.1.0-alpha.1"
VERSION = __version__
