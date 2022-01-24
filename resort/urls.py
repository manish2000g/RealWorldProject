from django.urls import path
from . import views
urlpatterns = [
    path('home', views.home),
    path('activity_type_form', views.activity_type_form),
    path('get_activity_type', views.get_activity_type),
    path('delete_activity_type/<int:activity_type_id>', views.delete_activity_type),
    path('update_activity_type/<int:activity_type_id>', views.update_activity_type),

    path('activity_form', views.activity_form),
    path('get_activity', views.get_activity),
    path('delete_activity/<int:activity_id>', views.delete_activity),
    path('update_activity/<int:activity_id>', views.update_activity),
    path('activities_view', views.view_activities),

    path('delete_cart_activity/<int:cart_id>', views.delete_cart_activity),
    path('add_to_cart/<int:activity_id>', views.add_to_cart),
    path('user_cart', views.view_cart_activities),

    path('order_form/<int:activity_id>/<int:cart_id>', views.order_form),
    path('user_order', views.user_order),
    path('esewa_verify', views.esewa_verify),

]
