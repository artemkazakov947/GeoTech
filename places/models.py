from django.contrib.gis.db import models


class Place(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField()
    geom = models.PointField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
