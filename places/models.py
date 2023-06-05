from django.contrib.gis.db import models


class Place(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField()
    geom = models.PointField()

    def __str__(self):
        return f"{self.name} : {self.geom.wkt}"
