# urls.py es el archivo de configuración de rutas del proyecto Django, donde se definen las URL que corresponden a cada vista o aplicación dentro del proyecto. y redirige a vault.urls para manejar las rutas relacionadas con los snippets.

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vault.urls')), #aqui decimos todas las rutas se las paso a vault.urls.
]
