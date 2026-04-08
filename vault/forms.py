from django import forms
from .models import Snippet


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ['titulo', 'lenguaje', 'categoria', 'descripcion', 'codigo', 'destacado']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Git Alias para limpiar ramas'
            }),
            'lenguaje': forms.Select(attrs={
                'class': 'form-select'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe qué hace este snippet...'
            }),
            'codigo': forms.Textarea(attrs={
                'class': 'form-control font-monospace',
                'rows': 12,
                'placeholder': 'Pega aquí el código o comando...'
            }),
            'destacado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
