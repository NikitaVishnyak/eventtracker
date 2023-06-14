from django.urls import path

from users.views import RegisterUser, LoginUser, logout_user, ProfileViewSet

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='sign up'),
    path('logout/', logout_user, name='logout'),
    path('api/v1/profile/<str:user_slug>/', ProfileViewSet.as_view(), name='profile'),
]
