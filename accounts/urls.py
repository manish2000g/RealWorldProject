from . import views
from django.urls import path
urlpatterns=[
   path('',views.user_login),
   path('login/',views.user_login),
   path('register/',views.user_register),
   path('logout/',views.user_logout)

]

