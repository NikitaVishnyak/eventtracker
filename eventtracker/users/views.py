from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from rest_framework.views import APIView

from verify_email.email_handler import send_verification_email

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
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        send_verification_email(self.request, form)

        return redirect('email_sent')


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


class RequestNewEmailView(TemplateView):
    template_name = 'request_new_email.html'


class EmailSentView(TemplateView):
    template_name = 'new_email_sent.html'