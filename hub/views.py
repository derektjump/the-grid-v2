from django.views.generic import TemplateView


class HubDashboardView(TemplateView):
    """
    Main landing page for The Grid hub.
    Displays app tiles for all integrated tools and applications.
    """
    template_name = 'hub/dashboard.html'
