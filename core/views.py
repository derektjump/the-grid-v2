from django.http import JsonResponse


def health_check(request):
    """
    Simple health check endpoint for monitoring and deployment verification.
    Returns a JSON response indicating the service is healthy.
    """
    return JsonResponse({
        'status': 'healthy',
        'service': 'The Grid',
    })
