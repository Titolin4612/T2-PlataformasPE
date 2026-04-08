from django import forms
from .models import Snippet


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ['titulo', 'lenguaje', 'categoria', 'descripcion', 'codigo', 'destacado']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 placeholder:text-slate-500 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/30',
                'placeholder': 'Ej: Git Alias para limpiar ramas'
            }),
            'lenguaje': forms.Select(attrs={
                'class': 'w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/30'
            }),
            'categoria': forms.Select(attrs={
                'class': 'w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/30'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 placeholder:text-slate-500 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/30',
                'rows': 4,
                'placeholder': 'Describe qué hace este snippet...'
            }),
            'codigo': forms.Textarea(attrs={
                'class': 'w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 font-mono text-slate-100 placeholder:text-slate-500 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/30',
                'rows': 12,
                'placeholder': 'Pega aquí el código o comando...'
            }),
            'destacado': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 rounded border-slate-600 bg-slate-900 text-indigo-500 focus:ring-indigo-500/50'
            }),
        }
