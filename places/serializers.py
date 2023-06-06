from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from places.models import Place


class PlaceSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Place
        fields = ("id", "name", "description", "geom")
        geo_field = "geom"


class CreatePlaceSerializer(serializers.ModelSerializer):
    longitude = serializers.FloatField(write_only=True)
    latitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Place
        fields = ("id", "name", "description", "longitude", "latitude")

    def validate(self, attrs):
        long = attrs.get('longitude')
        lat = attrs.get('latitude')
        name = attrs.get("name")
        point = Point(long, lat, srid=4326)
        old_place = Place.objects.filter(name=name).filter(geom__exact=point)
        if old_place:
            raise serializers.ValidationError("This place already exist")
        data = super().validate(attrs)
        return data

    def create(self, validated_data):
        long = validated_data.pop("longitude")
        lat = validated_data.pop("latitude")
        point = Point(long, lat, srid=4326)
        validated_data["geom"] = point
        return super().create(validated_data)
