from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
urlpatterns= [
    path('', views.user_login),
    path('login/', views.user_login),
    path('register/', views.user_register),
    path('logout/', views.user_logout),
    path('profile', views.profile),
    path('admins/users', views.get_users),
    path('admins/admins', views.get_admins),
    path('promote_user/<int:user_id>', views.promote_user),
    path('demote_user/<int:user_id>', views.demote_user),
    path('deactivate_user/<int:user_id>', views.deactivate_user),
    path('deactivate_admin/<int:user_id>', views.deactivate_admin),
    path('activate_user/<int:user_id>', views.activate_user),
    path('activate_admin/<int:user_id>', views.activate_admin),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/pwchange.html')),
    path('password_change-done/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/pwchange_done.html'), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset"),
    path('password_reset_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('reset/done',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
         name="password_reset_complete"),

]
