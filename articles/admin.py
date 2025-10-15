from django.contrib import admin
from .models import Article, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    
    def has_module_permission(self, request):
        """Allow all staff to see categories"""
        return request.user.is_staff


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    
    def has_module_permission(self, request):
        """Allow all staff to see tags"""
        return request.user.is_staff


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "is_featured", "published_at")
    list_filter = ("category", "is_featured", "published_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    date_hierarchy = "published_at"
    ordering = ("-published_at",)

    def get_queryset(self, request):
        """Filter articles based on user role"""
        qs = super().get_queryset(request)
        
        # Superusers see everything
        if request.user.is_superuser:
            return qs
        
        # Admins and Editors see all articles
        if request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
            return qs
        
        # Authors only see their own articles
        if request.user.groups.filter(name='Author').exists():
            return qs.filter(author=request.user)
        
        return qs
    
    def has_module_permission(self, request):
        """Allow all staff to see the Articles module"""
        return request.user.is_staff
    
    def has_add_permission(self, request):
        """All staff can add articles"""
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        """
        - Authors can edit their own articles
        - Editors and Admins can edit all articles
        """
        if request.user.is_superuser:
            return True
        
        if request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
            return True
        
        # If checking list permission (obj is None)
        if obj is None:
            return True
        
        # Authors can only edit their own
        return obj.author == request.user
    
    def has_delete_permission(self, request, obj=None):
        """Only Editors and Admins can delete articles"""
        if request.user.is_superuser:
            return True
        
        return request.user.groups.filter(name__in=['Admin', 'Editor']).exists()
    
    def has_view_permission(self, request, obj=None):
        """
        - Authors can view their own articles
        - Editors and Admins can view all articles
        """
        if request.user.is_superuser:
            return True
        
        if request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
            return True
        
        if obj is None:
            return True
        
        # Authors can view their own
        return obj.author == request.user
    
    def save_model(self, request, obj, form, change):
        """Automatically set author to current user for new articles"""
        if not change:  # If creating new article
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request, obj=None):
        """Make author field readonly for non-admins"""
        if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
            return []
        return ['author'] if obj else []
    
    @admin.action(description='Mark as featured')
    def mark_featured(self, request, queryset):
        """Mark selected articles as featured (Editors and Admins only)"""
        if not (request.user.is_superuser or request.user.groups.filter(name__in=['Admin', 'Editor']).exists()):
            self.message_user(request, "You don't have permission to feature articles.", level='error')
            return
        
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} article(s) marked as featured.')
    
    @admin.action(description='Remove featured status')
    def unmark_featured(self, request, queryset):
        """Remove featured status (Editors and Admins only)"""
        if not (request.user.is_superuser or request.user.groups.filter(name__in=['Admin', 'Editor']).exists()):
            self.message_user(request, "You don't have permission to unfeature articles.", level='error')
            return
        
        queryset.update(is_featured=False)
        self.message_user(request, f'{queryset.count()} article(s) unfeatured.')
    
    def get_actions(self, request):
        """Show feature actions only to Editors and Admins"""
        actions = super().get_actions(request)
        
        if not (request.user.is_superuser or request.user.groups.filter(name__in=['Admin', 'Editor']).exists()):
            # Remove feature actions for Authors
            actions.pop('mark_featured', None)
            actions.pop('unmark_featured', None)
        
        return actions
    
    actions = ['mark_featured', 'unmark_featured']