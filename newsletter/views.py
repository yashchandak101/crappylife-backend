from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Subscriber
from .serializers import SubscriberSerializer
from .utils import send_newsletter

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [permissions.AllowAny]  # or change based on access

    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def send_newsletter(self, request):
        subject = request.data.get("subject")
        message = request.data.get("message")
        if not subject or not message:
            return Response(
                {"error": "Subject and message are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscribers = Subscriber.objects.filter(is_active=True).values_list("email", flat=True)
        if not subscribers:
            return Response(
                {"error": "No active subscribers found."},
                status=status.HTTP_404_NOT_FOUND
            )
        send_newsletter(subject, message, list(subscribers))
        return Response({"status": "Newsletter sent"}, status=status.HTTP_200_OK)