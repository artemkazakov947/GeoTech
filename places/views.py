from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from places.models import Place
from places.serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    @action(methods=["GET"], url_path="nearest_place", detail=False)
    def nearest_place(self, request: Request) -> Response:
        long = request.GET.get("long", 0)
        lat = request.GET.get("lat", 0)
        if long and lat:
            users_point = Point(float(long), float(lat), srid=4326)

            nearest_place = Place.objects.annotate(
                distance=Distance("geom", users_point)
            ).order_by("distance")[:1][0]

            serialized = PlaceSerializer(nearest_place, many=False)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
