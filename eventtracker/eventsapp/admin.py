from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Events, EventCategories

User = get_user_model()


class EventsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Events, EventsAdmin)
admin.site.register(EventCategories)
