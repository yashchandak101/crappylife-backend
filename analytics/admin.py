from django.contrib import admin
from .models import PageView, ArticleView, EventClick

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ("path", "user", "ip_address", "created_at")
    list_filter = ("created_at",)
    search_fields = ("path", "user__username", "ip_address")

@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ("article", "user", "ip_address", "viewed_at")
    list_filter = ("viewed_at", "article")
    search_fields = ("article__title", "user__username", "ip_address")

@admin.register(EventClick)
class EventClickAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "ip_address", "clicked_at")
    list_filter = ("clicked_at", "event")
    search_fields = ("event__title", "user__username", "ip_address")
