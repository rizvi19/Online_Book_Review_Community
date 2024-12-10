from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
    # path("logout/", auth_views.LogoutView.as_view(next_page='/'), name="logout"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('logout/', views.logout_view, name='logout'),
]
