from cities_light.models import City
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, TemplateView
from rest_framework import viewsets
from django.shortcuts import render, redirect
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.views import APIView

from .forms import AddEventForm
from .models import EventCategories, Events
from .permissions import IsEventOrganizerOrAdmin
from .serializers import EventCategoriesSerializer, EventsSerializer


class EventCategoriesViewSet(viewsets.ModelViewSet):
    queryset = EventCategories.objects.all()
    serializer_class = EventCategoriesSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    title = "eventtracker"

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action in ['partial_update', 'update']:
            permission_classes = [IsEventOrganizerOrAdmin]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this event.")

        return super().destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not request.user.is_staff or (
                instance.organizer != request.user and 'is_confirmed' not in request.data and not request.data
        ['is_confirmed']):
            raise PermissionDenied("You do not have permission to edit this event.")

        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not request.user.is_staff or (
                instance.organizer != request.user and 'is_confirmed' not in request.data and not request.data['is_confirmed']):
            raise PermissionDenied("You do not have permission to edit this event.")

        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        events = self.get_queryset().filter(is_confirmed=True).order_by('-id')
        return render(request, 'index.html', {'events': events})


class CityView(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        events = Events.objects.select_related('country').order_by('country__name')

        data = {}
        for event in events:
            country_name = event.country.name
            if country_name not in data:
                data[country_name] = []

            city_name = event.city.name
            if city_name not in [e.city.name for e in data[country_name]]:
                data[country_name].append(event)

        return render(request, 'cities.html', {'data': data})


class CityEventsView(APIView):
    def get(self, request, city_name):
        city_events = Events.objects.filter(city__name=city_name)
        context = {
            'city_events': city_events,
            'city_name': city_name,
        }
        return render(request, 'city_events.html', context)


class AddEventView(CreateView):
    model = Events
    form_class = AddEventForm
    template_name = 'add_event.html'
    success_url = reverse_lazy('success_add')

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        form.instance.is_confirmed = False
        form.request = self.request
        response = super().form_valid(form)
        self.request.session['event_added'] = True
        return response


@require_GET
def get_cities(request):
    country_id = request.GET.get('country_id')

    cities = City.objects.filter(country_id=country_id)
    serialized_cities = [{'id': city.id, 'name': city.name} for city in cities]
    print(serialized_cities)
    return JsonResponse(serialized_cities, safe=False, json_dumps_params={'ensure_ascii': False})


class SuccessAddView(TemplateView):
    template_name = 'success_add.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('event_added'):
            raise Http404("Event not added")
        return super().dispatch(request, *args, **kwargs)


def set_home_page(request):
    return redirect('home')

