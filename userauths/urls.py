from django.urls import path, include
from django.contrib.auth import views as auth_views
from userauths import views
from . import views

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.register_view, name="sign-up"),
    path("sign-in/", views.login_view, name="sign-in"),
    path("sign-out/", views.logout_view, name="sign-out"),
    path('register/', views.register_vendor, name='register_vendor'),
    path('profile/update/', views.profile_update, name='profile-update'),
    
    # Include the default authentication views
    path("", include('django.contrib.auth.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  # Updated name
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Add a custom password reset view with a custom template
]


