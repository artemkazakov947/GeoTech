from rest_framework_gis.serializers import GeoFeatureModelSerializer

from places.models import Place


class PlaceSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Place
        fields = ("id", "name", "description", "geom")
        geo_field = "geom"
