from .models import PageView
import threading

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.path.startswith("/admin"):  # don’t track admin
            ip = request.META.get("REMOTE_ADDR")
            user = request.user if request.user.is_authenticated else None
            ua = request.META.get("HTTP_USER_AGENT", "")

            def save_pageview(path, user, ip_address, user_agent):
                PageView.objects.create(
                    path=path,
                    user=user,
                    ip_address=ip_address,
                    user_agent=user_agent
                )

            threading.Thread(
                target=save_pageview,
                args=(request.path, user, ip, ua)
            ).start()

        return response
