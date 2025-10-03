from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id", "title", "slug", "description",
            "date", "location", "image",
            "created_at", "updated_at"
        ]
