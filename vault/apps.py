from django.apps import AppConfig


# CONFIGURACIÓN DE APP: registra la aplicación vault dentro del proyecto Django.
class VaultConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vault'
