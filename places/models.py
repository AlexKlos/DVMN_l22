from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name='Название')
    short_description = models.TextField(verbose_name='Краткое описание', blank=True)
    long_description = models.TextField(verbose_name='Полное описание', blank=True)
    lng = models.FloatField(verbose_name='Долгота')
    lat = models.FloatField(verbose_name='Широта')

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    image = models.ImageField(upload_to='places/', verbose_name='Изображение')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.place.title}"