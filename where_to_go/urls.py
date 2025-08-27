from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from places import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_index),
    path('places/<int:place_id>.json/', views.get_place_details, name='place_details'),
    path('places/<int:place_id>/', views.get_place_details, name='place_details'),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)