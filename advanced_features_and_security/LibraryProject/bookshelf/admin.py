from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.admin import UserAdmin

# Book admin interface
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Fields to search in the admin interface
    search_fields = ('title', 'author')
    
    # Fields to filter by in the admin interface
    list_filter = ('publication_year',)
    
# Custom user model admin interface
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'date_of_birth', 'profile_photo', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'date_of_birth', 'profile_photo', 'is_active', 'is_staff')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',) 
    
# Register the Book model with the admin interface
admin.site.register(Book, BookAdmin)
# Register the CustomUser model with the admin interface
admin.site.register(CustomUser, CustomUserAdmin) 

