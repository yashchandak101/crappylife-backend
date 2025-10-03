from .models import Notification

def create_notification(user, title, message, notif_type="system", link=None):
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notif_type=notif_type,
        link=link
    )
