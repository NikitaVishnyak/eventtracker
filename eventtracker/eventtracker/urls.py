from django.contrib import admin
from django.urls import path, include

from eventsapp.views import EventsViewSet, CityEventsView, CityView, AddEventView, get_cities, \
    SuccessAddView, set_home_page

urlpatterns = [
    path('', set_home_page, name='set_home_page'),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/events/', EventsViewSet.as_view({'get': 'list'}), name='home'),
    path('api/v1/cities/', CityView.as_view({'get': 'list'}), name='cities_list'),
    path('api/v1/<str:city_name>/events/', CityEventsView.as_view(), name='city_events'),
    path('', include('users.urls')),
    path('add-event/', AddEventView.as_view(), name='add_event'),
    path('get-cities/', get_cities, name='get_cities'),
    path('add-event/success-add/', SuccessAddView.as_view(), name='success_add'),
]
