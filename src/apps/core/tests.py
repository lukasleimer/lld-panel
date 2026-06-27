from django.test import TestCase, Client
from django.urls import reverse
from config.version import VERSION


class HealthCheckViewTest(TestCase):
    """Tests für Health Check Endpoint"""
    
    def setUp(self):
        self.client = Client()
    
    def test_health_check_status_code(self):
        """Health Check sollte 200 zurückgeben"""
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
    
    def test_health_check_json_response(self):
        """Health Check sollte JSON mit 'status': 'ok' zurückgeben"""
        response = self.client.get('/health/')
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertIn('version', data)
        self.assertIn('timestamp', data)
    
    def test_health_check_version_from_config(self):
        """Health Check sollte Version aus config.version nutzen"""
        response = self.client.get('/health/')
        data = response.json()
        self.assertEqual(data['version'], VERSION)


class DashboardViewTest(TestCase):
    """Tests für Dashboard View"""
    
    def setUp(self):
        self.client = Client()
    
    def test_dashboard_status_code(self):
        """Dashboard sollte 200 zurückgeben"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_uses_correct_template(self):
        """Dashboard sollte core/dashboard.html nutzen"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'core/dashboard.html')
    
    def test_dashboard_context_has_title(self):
        """Dashboard Context sollte page_title enthalten"""
        response = self.client.get('/')
        self.assertEqual(response.context['page_title'], 'Dashboard')


class CoreContextProcessorTest(TestCase):
    """Tests für Context Processor"""
    
    def setUp(self):
        self.client = Client()
    
    def test_core_context_in_template(self):
        """Core Context sollte in jedem Template verfügbar sein"""
        response = self.client.get('/')
        self.assertEqual(response.context['app_name'], 'LLD Panel')
        self.assertEqual(response.context['app_version'], VERSION)
        self.assertEqual(response.context['environment'], 'Development')
