from django.urls import path
from . import views

urlpatterns = [
  path('admin_dashboard/', views.admin_dashboard),
  # path('show_order/', views.get_order),
  # path("deliver/<int:id>", views.delivered),
  # path("pending/<int:id>", views.pending)

]
