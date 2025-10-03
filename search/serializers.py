from rest_framework import serializers
from articles.models import Article
from events.models import Event

class ArticleSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "title", "slug", "cover_image", "content", "category", "tags", "published_at"]

class EventSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "title", "slug", "image", "description", "date", "location"]
