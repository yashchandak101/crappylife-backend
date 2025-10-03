from rest_framework import serializers
from .models import Article, Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id", "title", "slug", "author",
            "category", "tags", "content",
            "cover_image", "is_featured",
            "published_at", "updated_at"
        ]

        def get_image(self, obj):
                request = self.context.get("request")
                if obj.image:
                    return request.build_absolute_uri(obj.image.url)
                return None
    
