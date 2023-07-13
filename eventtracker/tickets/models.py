from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Tickets(models.Model):
    event = models.ForeignKey('eventsapp.Events', on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField('Tickets')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.email}"

    def get_metadata(self):
        metadata = {
            'cart_id': self.id,
            'user_email': self.user.email,
        }
        return metadata
