from rest_framework import serializers
from .models import PageView, ArticleView, EventClick

class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        fields = "__all__"

class ArticleViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleView
        fields = "__all__"

class EventClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventClick
        fields = "__all__"
