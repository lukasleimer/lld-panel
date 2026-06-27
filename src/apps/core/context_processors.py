from django.utils import timezone
from config.version import VERSION


def core_context(request):
    """
    Globaler Context Processor - macht Daten in allen Templates verfügbar
    
    Nutzen:
    - App-Name und Version überall abrufbar (aus config.version)
    - Umgebungs-Info (Development/Production)
    - Aktuelle Benutzer-Info
    - Aktuelles Jahr für Copyright
    
    Version wird zentral aus src/config/version.py geladen.
    """
    return {
        'app_name': 'LLD Panel',
        'app_version': VERSION,  # Aus src/config/version.py
        'environment': 'Development',
        'current_user': request.user,
        'current_year': timezone.now().year,
    }
