"""
Custom middleware for The Grid
"""
from django.http import HttpResponse


class HealthCheckMiddleware:
    """
    Middleware to handle Azure health check requests without ALLOWED_HOSTS validation.

    Azure App Service health checks come from internal IPs (169.254.0.0/16 range)
    and use the internal container IP as the Host header instead of the public hostname.
    This causes Django's ALLOWED_HOSTS check to fail.

    This middleware intercepts health check requests to /robots933456.txt and returns
    a simple response without going through Django's security middleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Azure health checks request /robots933456.txt
        if request.path == '/robots933456.txt':
            return HttpResponse("OK", content_type="text/plain")

        # Also handle explicit health check endpoint
        if request.path == '/health/':
            # Let it pass through to the actual view
            pass

        return self.get_response(request)
