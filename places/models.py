from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description_short = models.CharField(max_length=400)
    description_long = models.TextField()
    lng = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    image = models.ImageField(upload_to='places/')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.place.title}"