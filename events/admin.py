from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "location")
    list_filter = ("date",)
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-date",)
