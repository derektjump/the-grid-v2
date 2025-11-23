from django.urls import path
from .views import HubDashboardView

app_name = 'hub'

urlpatterns = [
    path('', HubDashboardView.as_view(), name='dashboard'),
]
