from django.apps import AppConfig


class WebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webapp'
    verbose_name = "Web App"  # This is the name that will be displayed in th
# admin interface. You can change it to whatever you like.
