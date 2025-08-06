from django.contrib import admin

from .models import Place


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    pass

admin.site.register(Place)
