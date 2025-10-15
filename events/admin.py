from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "location", "get_organizer")
    list_filter = ("date",)
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-date",)
    
    def get_organizer(self, obj):
        """Display the organizer/creator of the event"""
        # Assuming you have an organizer or created_by field
        # If not, you might need to add it to your Event model
        return getattr(obj, 'organizer', getattr(obj, 'created_by', 'N/A'))
    get_organizer.short_description = 'Organizer'
    
    def get_queryset(self, request):
        """Filter events based on user role"""
        qs = super().get_queryset(request)
        
        # Superusers see everything
        if request.user.is_superuser:
            return qs
        
        # Admins and Editors see all events
        if request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
            return qs
        
        # Authors only see their own events (if you have an organizer/created_by field)
        # Uncomment and adjust the field name based on your Event model:
        # if hasattr(qs.model, 'organizer'):
        #     return qs.filter(organizer=request.user)
        # elif hasattr(qs.model, 'created_by'):
        #     return qs.filter(created_by=request.user)
        
        return qs
    
    def has_module_permission(self, request):
        """Allow all staff to see the Events module"""
        return request.user.is_staff
    
    def has_add_permission(self, request):
        """All staff can add events"""
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        """
        - Authors can edit their own events (if applicable)
        - Editors and Admins can edit all events
        """
        if request.user.is_superuser:
            return True
        
        if request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
            return True
        
        # If checking list permission (obj is None)
        if obj is None:
            return True
        
        # If your Event model has an organizer or created_by field:
        # Uncomment and adjust based on your model:
        # if hasattr(obj, 'organizer'):
        #     return obj.organizer == request.user
        # elif hasattr(obj, 'created_by'):
        #     return obj.created_by == request.user
        
        # Default: Authors can edit if they're staff
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        """Only Editors and Admins can delete events"""
        if request.user.is_superuser:
            return True
        
        return request.user.groups.filter(name__in=['Admin', 'Editor']).exists()
    
    def has_view_permission(self, request, obj=None):
        """All staff can view events"""
        return request.user.is_staff
    
    def save_model(self, request, obj, form, change):
        """
        Automatically set organizer/created_by to current user for new events
        Uncomment and adjust based on your Event model fields:
        """
        if not change:  # If creating new event
            # if hasattr(obj, 'organizer'):
            #     obj.organizer = request.user
            # elif hasattr(obj, 'created_by'):
            #     obj.created_by = request.user
            pass
        
        super().save_model(request, obj, form, change)
    
    @admin.action(description='Mark as featured')
    def mark_featured(self, request, queryset):
        """Mark selected events as featured (Editors and Admins only)"""
        if not (request.user.is_superuser or request.user.groups.filter(name__in=['Admin', 'Editor']).exists()):
            self.message_user(request, "You don't have permission to feature events.", level='error')
            return
        
        # Check if Event model has is_featured field
        if hasattr(queryset.model, 'is_featured'):
            queryset.update(is_featured=True)
            self.message_user(request, f'{queryset.count()} event(s) marked as featured.')
        else:
            self.message_user(request, "Event model doesn't have is_featured field.", level='warning')
    
    def get_actions(self, request):
        """Show feature actions only to Editors and Admins"""
        actions = super().get_actions(request)
        
        if not (request.user.is_superuser or request.user.groups.filter(name__in=['Admin', 'Editor']).exists()):
            # Remove feature actions for Authors
            actions.pop('mark_featured', None)
        
        return actions
    
    actions = ['mark_featured']