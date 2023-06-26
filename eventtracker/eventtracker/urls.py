from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from eventsapp.views import set_home_page

urlpatterns = [
    path('', set_home_page, name='set_home_page'),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('', include('eventsapp.urls')),
    path('', include('users.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

