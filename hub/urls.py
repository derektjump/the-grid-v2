from django.urls import path
from .views import HubDashboardView, AboutView

app_name = 'hub'

urlpatterns = [
    path('', HubDashboardView.as_view(), name='dashboard'),
    path('about/', AboutView.as_view(), name='about'),
]
