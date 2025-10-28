from django.apps import AppConfig
from .models import BlogPost
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Bookshelf application configuration
class BookshelfConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bookshelf"
    
# BlogPost model configuration
class BlogPostConfig(AppConfig):
    name = 'blog'
    
    def ready(self):
        # Connect the signal to create default groups
        post_migrate.connect(create_groups, sender=self) 
        
def create_groups(sender, **kwargs):
    # Create groups and keep track of whether they were created
    editors, editors_created = Group.objects.get_or_create(name='Editors')
    viewers, viewers_created = Group.objects.get_or_create(name='Viewers')
    admins, admins_created = Group.objects.get_or_create(name='Admin') 
    
    try:
        if editors_created:
            # Assign permissions to editors
            editors.permissions.set([
                Permission.objects.get(codename='can_view'),
                Permission.objects.get(codename='can_edit'),
                Permission.objects.get(codename='can_create'),
            ])
            
        if viewers_created:
            # Assign permissions to viewers
            viewers.permissions.set([
                Permission.objects.get(codename='can_view'),
            ])
            
        if admins_created:    
            # Assign all permissions to admins
            admins.permissions.set([
                Permission.objects.get(codename='can_view'),
                Permission.objects.get(codename='can_edit'),
                Permission.objects.get(codename='can_create'),
                Permission.objects.get(codename='can_delete'),
            ]) 
    except Permission.DoesNotExist as e:
        print(f"Permission error: {e}")        
