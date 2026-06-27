from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from config.version import VERSION


def dashboard(request):
    """Hauptseite / Dashboard des LLD Panels"""
    context = {
        'page_title': 'Dashboard',
    }
    return render(request, 'core/dashboard.html', context)


def health_check(request):
    """Health Check Endpoint für Monitoring"""
    data = {
        'status': 'ok',
        'version': VERSION,
        'timestamp': timezone.now().isoformat(),
        'environment': 'development',
    }
    return JsonResponse(data)


def page_not_found(request, exception=None):
    """404 Error Handler"""
    return render(request, '404.html', status=404)


def server_error(request):
    """500 Error Handler"""
    return render(request, '500.html', status=500)
