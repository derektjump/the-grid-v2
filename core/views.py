from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings


def health_check(request):
    """
    Simple health check endpoint for monitoring and deployment verification.
    Returns a JSON response indicating the service is healthy.
    """
    return JsonResponse({
        'status': 'healthy',
        'service': 'The Grid',
    })


def custom_logout(request):
    """
    Custom logout view for Azure AD / OIDC.
    Logs out the user from Django session and redirects to home page.

    Note: This does NOT log out from Azure AD itself. The user will still
    have an active Azure AD session. To fully log out from Azure AD, you would
    need to redirect to the Azure AD logout endpoint:
    https://login.microsoftonline.com/{tenant}/oauth2/v2.0/logout
    """
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
