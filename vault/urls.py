# urls.py define las rutas para las vistas relacionadas con los snippets, incluyendo la lista de snippets, detalles, creación, edición y eliminación.
# urls.py recibe lo que quiere el usuario y lo manda a views.py para que haga el proceso necesario.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.snippet_list, name='snippet_list'),
    path('snippet/<int:pk>/', views.snippet_detail, name='snippet_detail'),
    path('crear/', views.snippet_create, name='snippet_create'),
    path('editar/<int:pk>/', views.snippet_update, name='snippet_update'),
    path('eliminar/<int:pk>/', views.snippet_delete, name='snippet_delete'),
]
