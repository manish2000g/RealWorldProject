from django.urls import path
from . import views

urlpatterns = [
  path('admin_dashboard/',views.admin_dashboard),

    ]