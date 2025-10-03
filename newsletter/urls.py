from rest_framework.routers import DefaultRouter
from .views import SubscriberViewSet

router = DefaultRouter()
router.register("subscribers", SubscriberViewSet, basename="subscribers")

urlpatterns = router.urls
