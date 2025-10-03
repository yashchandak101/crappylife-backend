"""
URL configuration for crappylife project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
# Example: router.register(r'items', ItemsViewSet)  # Register your viewsets here

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(router.urls)),
    path("api/accounts/", include("accounts.urls")),
    path("api/articles/", include("articles.urls")),
    path("api/events/", include("events.urls")),
    path("api/search/", include("search.urls")),
    path("api/newsletter/", include("newsletter.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/notifications/", include("notifications.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


