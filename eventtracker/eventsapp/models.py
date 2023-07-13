import requests
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

from eventtracker import settings
from tickets.models import Tickets


class Events(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    organizer = models.ForeignKey('users.CustomUsers', on_delete=models.CASCADE)
    ticket_quantity = models.PositiveIntegerField(default=0)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False, blank=True)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=150)
    category = models.ForeignKey('EventCategories', related_name='caterories', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('concrete_event', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'slug': self.slug})

    def available_tickets(self):
        return self.ticket_quantity - Tickets.objects.filter(event=self).count()

    def get_coordinates(self):
        full_address = f"{self.address}, {self.city.display_name}"

        params = {
            'key': settings.MAPQUEST_API_KEY,
            'location': full_address,
            'maxResults': 1
        }

        response = requests.get('https://www.mapquestapi.com/geocoding/v1/address', params=params)
        data = response.json()

        if data['results']:
            latitude = data['results'][0]['locations'][0]['latLng']['lat']
            longitude = data['results'][0]['locations'][0]['latLng']['lng']
            return latitude, longitude
        else:
            return None

    class Meta:
        verbose_name_plural = 'Events'


@receiver(post_save, sender=Events)
def create_event_slug(sender, instance, created, **kwargs):
    if created:
        instance.slug = slugify(f"{instance.title}")
        instance.save()


class EventCategories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_events', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = 'EventCategories'
