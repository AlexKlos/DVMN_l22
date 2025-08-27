from adminsortable2.admin import SortableStackedInline, SortableAdminBase
from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from .models import Place, PlaceImage


class PlaceImageInline(SortableStackedInline):
    model = PlaceImage
    extra = 1
    fields = ('image', 'image_preview')
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        return format_html('<img src="{}" style="height: 80px;"/>', obj.image.url)


class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('title', 'id',)
    inlines = [PlaceImageInline]
    search_fields = ['title']

admin.site.register(Place, PlaceAdmin)
