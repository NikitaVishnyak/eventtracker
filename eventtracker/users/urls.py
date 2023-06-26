from django.urls import path, include

from users.views import LoginUser, logout_user, ProfileViewSet, EmailSentView, RequestNewEmailView, \
    RegisterUser

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='sign up'),
    path('logout/', logout_user, name='logout'),
    path('verification/', include('verify_email.urls')),
    path('api/v1/profile/<str:user_slug>/', ProfileViewSet.as_view(), name='profile'),
    path('email-sent/', EmailSentView.as_view(), name='email_sent'),
    path('verification/user/verify-email/request-new-link/', RequestNewEmailView.as_view(), name='request_new_email'),
]
