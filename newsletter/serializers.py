from rest_framework import serializers
from .models import Subscriber

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ["id", "name", "email", "subscribed_at", "is_active"]
        read_only_fields = ["id", "subscribed_at", "is_active"]
