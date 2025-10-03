from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from .models import Event
from .serializers import EventSerializer
from rest_framework.response import Response

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by("-date")
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "pk"  # Default lookup field is 'pk' (id)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()

        # Try to find by slug first
        event = queryset.filter(slug=pk).first()

        # If not found by slug, try by ID
        if not event:
            event = get_object_or_404(queryset, pk=pk)

        serializer = self.get_serializer(event)
        return Response(serializer.data)
