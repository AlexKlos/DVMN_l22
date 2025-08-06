from django.contrib import admin
from django.utils.html import format_html

from .models import Place, PlaceImage


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ('order',)
    fields = ('order', 'image', 'image_preview')
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        return format_html('<img src="{}" style="height: 80px;"/>', obj.image.url)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [PlaceImageInline]

admin.site.register(Place, PlaceAdmin)
