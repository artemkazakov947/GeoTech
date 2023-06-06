from rest_framework.routers import DefaultRouter

from places.views import PlaceViewSet

router = DefaultRouter()
router.register("places", PlaceViewSet)

urlpatterns = router.urls

app_name = "places"
