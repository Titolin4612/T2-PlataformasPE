from django.contrib import admin
from .models import Snippet


# ADMIN REGISTRATION: habilita la gestión del modelo Snippet desde el panel administrativo.
@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    # LISTADO ADMIN: columnas, filtros y búsqueda para revisar snippets con rapidez.
    list_display = ('titulo', 'lenguaje', 'categoria', 'destacado', 'creado_en')
    list_filter = ('lenguaje', 'categoria', 'destacado')
    search_fields = ('titulo', 'descripcion', 'codigo')
