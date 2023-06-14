from rest_framework import serializers

from .models import EventCategories, Events


class EventCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategories
        fields = "__all__"


class EventsSerializer(serializers.ModelSerializer):
    organizer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_confirmed = serializers.HiddenField(default=False)

    class Meta:
        model = Events
        fields = "__all__"
