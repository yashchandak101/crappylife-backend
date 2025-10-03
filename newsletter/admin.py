from django.contrib import admin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from .models import Subscriber, Newsletter
from .utils import send_newsletter
from django import forms

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ["subject", "message"]

@admin.action(description="Send selected newsletters to all active subscribers")
def send_newsletter_to_subscribers(modeladmin, request, queryset):
    recipient_list = list(
        Subscriber.objects.filter(is_active=True).values_list('email', flat=True)
    )
    print("DEBUG → Subscribers:", recipient_list)  # Debug
    for newsletter in queryset:
        print("DEBUG → Sending:", newsletter.subject)  # Debug
        send_newsletter(
            newsletter.subject,
            newsletter.message,
            recipient_list
        )
        
class NewsletterAdmin(admin.ModelAdmin):
    actions = [send_newsletter_to_subscribers]

admin.site.register(Newsletter, NewsletterAdmin)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "name", "is_active", "subscribed_at")
    list_filter = ("is_active", "subscribed_at")
    search_fields = ("email", "name")
