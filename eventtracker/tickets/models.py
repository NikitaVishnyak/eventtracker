from datetime import timedelta

from django.db import models
from django.utils import timezone


class Tickets(models.Model):
    event = models.ForeignKey('eventsapp.Events', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUsers', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reservation_duration = models.DurationField(default=timedelta(minutes=15))
    reservation_time = models.DateTimeField(null=True, blank=True)
    is_reserved = models.BooleanField(default=False)


    def reserve_ticket(self, user):
        if self.reservation_time is None:
            self.reservation_time = timezone.now()
            self.user = user
            self.is_reserved = True
            self.save()

    def is_reservation_expired(self):
        if self.reservation_time is None:
            return False

        expiration_time = self.reservation_time + self.reservation_duration
        return timezone.now() > expiration_time

    def release_reservation(self):
        if self.is_reservation_expired():
            self.is_reserved = False
            self.user = None
            self.reservation_time = None
            self.save()
