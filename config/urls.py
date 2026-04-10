from django.urls import include, path
from vault.admin import vault_admin_site

# ENRUTAMIENTO PRINCIPAL: expone el panel admin y delega el sitio público a la app vault.
urlpatterns = [
    path('admin/', vault_admin_site.urls),
    path('', include('vault.urls')),
]
