from django.urls import path, include

from eventsapp.views import EventsViewSet, CityViewSet, CityEventsViewSet, AddEventView, get_cities, SuccessAddView

urlpatterns = [
    path('api/v1/events/', EventsViewSet.as_view({'get': 'list'}), name='home'),
    path('api/v1/cities/', CityViewSet.as_view({'get': 'list'}), name='cities_list'),
    path('api/v1/<str:city_name>/events/', CityEventsViewSet.as_view(), name='city_events'),
    path('add-event/', AddEventView.as_view(), name='add_event'),
    path('get-cities/', get_cities, name='get_cities'),
    path('add-event/success-add/', SuccessAddView.as_view(), name='success_add'),
    path('api/v1/events/<str:slug>/', EventsViewSet.as_view({'get': 'retrieve'}), name='concrete_event'),
]
