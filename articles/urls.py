from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register("articles", ArticleViewSet, basename="articles")
router.register("categories", CategoryViewSet, basename="categories")
router.register("tags", TagViewSet, basename="tags")

urlpatterns = router.urls
