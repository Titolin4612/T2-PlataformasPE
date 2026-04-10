from django import forms
from .models import Snippet

# ESTILOS REUTILIZABLES: concentran la apariencia base de inputs y selects del formulario CRUD.
BASE_INPUT_CLASSES = (
    'w-full rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 '
    'text-sm text-slate-100 outline-none transition placeholder:text-slate-500 '
    'focus:border-cyan-400/60 focus:ring-2 focus:ring-cyan-400/20'
)


# FORMULARIO CRUD: conecta el modelo Snippet con los campos visibles en crear y editar.
class SnippetForm(forms.ModelForm):
    class Meta:
        # VÍNCULO CON EL MODELO: define qué campos del snippet se editan desde la interfaz.
        model = Snippet
        fields = ['titulo', 'lenguaje', 'categoria', 'descripcion', 'codigo', 'destacado']
        # WIDGETS PERSONALIZADOS: ajustan clases, placeholders y tamaños según el tipo de entrada.
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': BASE_INPUT_CLASSES,
                'placeholder': 'Ej: Git Alias para limpiar ramas'
            }),
            'lenguaje': forms.Select(attrs={
                'class': f'{BASE_INPUT_CLASSES} appearance-none'
            }),
            'categoria': forms.Select(attrs={
                'class': f'{BASE_INPUT_CLASSES} appearance-none'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': f'{BASE_INPUT_CLASSES} min-h-28 resize-y',
                'rows': 4,
                'placeholder': 'Describe qué hace este snippet...'
            }),
            'codigo': forms.Textarea(attrs={
                'class': (
                    f'{BASE_INPUT_CLASSES} min-h-72 resize-y font-mono text-xs '
                    'leading-6 text-cyan-100'
                ),
                'rows': 12,
                'placeholder': 'Pega aquí el código o comando...'
            }),
            'destacado': forms.CheckboxInput(attrs={
                'class': (
                    'h-5 w-5 rounded border-white/15 bg-slate-950/70 text-cyan-400 '
                    'focus:ring-2 focus:ring-cyan-400/20 focus:ring-offset-0'
                )
            }),
        }
