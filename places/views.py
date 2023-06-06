from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from places.models import Place
from places.serializers import PlaceSerializer, CreatePlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_serializer_class(self):
        actions = {
            "create": CreatePlaceSerializer,
            "list": PlaceSerializer,
            "destroy": PlaceSerializer,
            "update": PlaceSerializer,
            "partial_update": PlaceSerializer,
            "retrieve": PlaceSerializer,
            "nearest_place": PlaceSerializer
        }

        return actions[self.action]

    def list(self, request, *args, **kwargs) -> Response:
        """List for all places"""
        return super().list(request)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="long",
                type=OpenApiTypes.DECIMAL,
                description="point's longitude",
                examples=[
                    OpenApiExample(
                        "Example",
                        description="provide longitude for point",
                        value="4.34878",
                    ),
                ],
            ),
            OpenApiParameter(
                name="lat",
                type=OpenApiTypes.DECIMAL,
                description="point's latitude",
                examples=[
                    OpenApiExample(
                        "Example",
                        description="provide latitude for point",
                        value="50.85045",
                    ),
                ],
            ),
        ],
        examples=[
            OpenApiExample("Example 1", description="Find nearest place to point", value="?long=4.34878&lat=50.85045"),
        ],
    )
    @action(methods=["GET"], url_path="nearest_place", detail=False)
    def nearest_place(self, request: Request) -> Response:
        """Endpoint which provide nearest place to given point (point gives by get params)"""
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
