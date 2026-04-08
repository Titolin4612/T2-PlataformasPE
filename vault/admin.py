from django.contrib import admin
from .models import Snippet


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'lenguaje', 'categoria', 'destacado', 'creado_en')
    list_filter = ('lenguaje', 'categoria', 'destacado')
    search_fields = ('titulo', 'descripcion', 'codigo')
