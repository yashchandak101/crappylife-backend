from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "article", "user", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("content", "user__username", "article__title")
    ordering = ("-created_at",)
