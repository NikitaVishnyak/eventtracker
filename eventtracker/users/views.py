from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.views import APIView

from users.forms import LoginUserForm, RegisterUserForm
from users.models import CustomUsers


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('home')


class ProfileViewSet(APIView):
    def get(self, request, user_slug):
        custom_user = CustomUsers.objects.get(slug=user_slug)
        context = {
            'custom_user': custom_user,
        }
        return render(request, 'profile.html', context)
