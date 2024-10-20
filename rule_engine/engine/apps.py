from django.apps import AppConfig
from django.db.models.signals import post_migrate

def clear_rules(sender, **kwargs):
    from .models import ASTNode
    print("Clearing all ASTNode objects...")
    ASTNode.objects.all().delete()

class EngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'engine'

    def ready(self):
        # Connect to post_migrate signal to clear rules after each migration or when the server starts
        post_migrate.connect(clear_rules, sender=self)