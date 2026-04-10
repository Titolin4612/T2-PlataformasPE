from django.contrib import admin
from django.urls import include, path

# ENRUTAMIENTO PRINCIPAL: expone el panel admin y delega el sitio público a la app vault.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vault.urls')),
]
