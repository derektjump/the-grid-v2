from django.views.generic import TemplateView


class HubDashboardView(TemplateView):
    """
    Main landing page for The Grid hub.
    Displays app tiles for all integrated tools and applications.
    """
    template_name = 'hub/dashboard.html'


class AboutView(TemplateView):
    """
    About page for The Grid.
    Tells the origin story, infrastructure, AI capabilities, and values.
    """
    template_name = 'hub/about.html'


class IntroView(TemplateView):
    """
    Animated intro/landing page for The Grid v2.0.
    Features Tron-style disc attack, de-rez effect, and laser construction.
    """
    template_name = 'hub/intro.html'
