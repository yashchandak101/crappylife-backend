from rest_framework import viewsets
from .models import PageView, ArticleView, EventClick
from .serializers import PageViewSerializer, ArticleViewSerializer, EventClickSerializer

class PageViewSet(viewsets.ModelViewSet):
    queryset = PageView.objects.all()
    serializer_class = PageViewSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = ArticleView.objects.all()
    serializer_class = ArticleViewSerializer

class EventClickViewSet(viewsets.ModelViewSet):
    queryset = EventClick.objects.all()
    serializer_class = EventClickSerializer
