from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"









from django.contrib.auth import logout
from django.shortcuts import redirect

# Custom Logout View
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout
