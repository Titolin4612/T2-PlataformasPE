from django.urls import path
from . import views

urlpatterns = [
    path('', views.snippet_list, name='snippet_list'),
    path('snippet/<int:pk>/', views.snippet_detail, name='snippet_detail'),
    path('crear/', views.snippet_create, name='snippet_create'),
    path('editar/<int:pk>/', views.snippet_update, name='snippet_update'),
    path('eliminar/<int:pk>/', views.snippet_delete, name='snippet_delete'),
]
