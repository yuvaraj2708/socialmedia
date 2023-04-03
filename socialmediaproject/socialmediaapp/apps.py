# In socialmediaapp/apps.py
from django.apps import AppConfig

class SocialMediaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'socialmediaapp'
    verbose_name = 'Social Media'

    # Add this line to specify the migration module for this app
    # It should match the value of `MIGRATION_MODULES` in admin/apps.py
    migration_module = 'socialmediaapp.migrations'
class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin'

    # Add this line to specify the migration module for this app
    # It should match the value of `MIGRATION_MODULES` in socialmediaapp/apps.py
    migration_module = 'admin.migrations'
