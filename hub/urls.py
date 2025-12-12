from django.urls import path
from .views import HubDashboardView, AboutView, IntroView

app_name = 'hub'

urlpatterns = [
    path('', IntroView.as_view(), name='intro'),
    path('dashboard/', HubDashboardView.as_view(), name='dashboard'),
    path('about/', AboutView.as_view(), name='about'),
]
