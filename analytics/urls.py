from rest_framework.routers import DefaultRouter
from .views import PageViewSet, ArticleViewSet, EventClickViewSet

router = DefaultRouter()
router.register("pageviews", PageViewSet)
router.register("articleviews", ArticleViewSet)
router.register("eventclicks", EventClickViewSet)

urlpatterns = router.urls
