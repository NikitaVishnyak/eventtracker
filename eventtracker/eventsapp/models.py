from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify


class Events(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    organizer = models.ForeignKey('users.CustomUsers', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False, blank=True)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('EventCategories', related_name='caterories', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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

    class Meta:
        verbose_name_plural = 'EventCategories'
