from adminsortable2.admin import SortableStackedInline, SortableAdminBase
from django.contrib import admin
from django.utils.html import format_html

from .models import Place, PlaceImage


class PlaceImageInline(SortableStackedInline):
    model = PlaceImage
    extra = 1
    fields = ('image', 'image_preview')
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 80px; max-width: 150px"/>', obj.image.url)


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('title', 'id',)
    inlines = [PlaceImageInline]
    search_fields = ['title']


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ("id", "place", "order", "image")
    search_fields = ("place__title",)
    autocomplete_fields = ("place",)
    list_filter = ("place",)
