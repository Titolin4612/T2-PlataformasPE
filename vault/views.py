from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from .forms import SnippetForm
from .models import Snippet


# ORDENAMIENTO DISPONIBLE: mapea cada opción del filtro con su etiqueta y criterio de base de datos.
SORT_OPTIONS = {
    'newest': {
        'label': 'Más recientes',
        'order_by': '-creado_en',
    },
    'oldest': {
        'label': 'Más antiguos',
        'order_by': 'creado_en',
    },
    'title_asc': {
        'label': 'Título A-Z',
        'order_by': 'titulo',
    },
    'title_desc': {
        'label': 'Título Z-A',
        'order_by': '-titulo',
    },
}


def snippet_list(request):
    # CRUD READ: arma el listado principal con filtros, orden y métricas del dashboard.
    base_queryset = Snippet.objects.all()
    snippets = base_queryset
    language_choices = dict(Snippet.LENGUAJES)
    category_choices = dict(Snippet.CATEGORIAS)

    # FILTROS DESDE QUERY PARAMS: se leen desde la URL para mantener enlaces compartibles.
    active_language = request.GET.get('language', '').strip()
    active_category = request.GET.get('category', '').strip()
    active_sort = request.GET.get('sort', 'newest').strip()

    # FILTRO POR LENGUAJE: solo aplica valores válidos definidos en el modelo.
    if active_language in language_choices:
        snippets = snippets.filter(lenguaje=active_language)
    else:
        active_language = ''

    # FILTRO POR CATEGORÍA: evita consultas con parámetros no reconocidos.
    if active_category in category_choices:
        snippets = snippets.filter(categoria=active_category)
    else:
        active_category = ''

    # ORDENAMIENTO SEGURO: usa una opción por defecto cuando el parámetro no coincide con las reglas.
    sort_config = SORT_OPTIONS.get(active_sort, SORT_OPTIONS['newest'])
    if active_sort not in SORT_OPTIONS:
        active_sort = 'newest'

    snippets = snippets.order_by(sort_config['order_by'])

    # MÉTRICAS DEL DASHBOARD: resumen para tarjetas superiores y ranking de lenguajes usados.
    total_count = base_queryset.count()
    featured_count = base_queryset.filter(destacado=True).count()
    top_languages = list(
        base_queryset.values('lenguaje')
        .annotate(total=Count('id'))
        .order_by('-total', 'lenguaje')[:3]
    )

    for item in top_languages:
        item['label'] = language_choices.get(item['lenguaje'], item['lenguaje'])

    # CONTEXTO DE LA VISTA: concentra datos del listado, filtros activos y contadores auxiliares.
    context = {
        'snippets': snippets,
        'language_choices': Snippet.LENGUAJES,
        'category_choices': Snippet.CATEGORIAS,
        'sort_choices': [(key, option['label']) for key, option in SORT_OPTIONS.items()],
        'active_language': active_language,
        'active_language_label': language_choices.get(active_language, ''),
        'active_category': active_category,
        'active_category_label': category_choices.get(active_category, ''),
        'active_sort': active_sort,
        'active_sort_label': sort_config['label'],
        'filters_active': bool(active_language or active_category or active_sort != 'newest'),
        'results_count': snippets.count(),
        'total_count': total_count,
        'featured_count': featured_count,
        'top_languages': top_languages,
    }
    return render(request, 'vault/snippet_list.html', context)


def snippet_detail(request, pk):
    # CRUD READ: recupera un snippet puntual o responde 404 si no existe.
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, 'vault/snippet_detail.html', {'snippet': snippet})


def snippet_create(request):
    # CRUD CREATE: procesa altas nuevas reutilizando el mismo formulario del modelo.
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save()
            return redirect('snippet_detail', pk=snippet.pk)
    else:
        # FORMULARIO VACÍO: se muestra cuando el usuario abre la pantalla de creación.
        form = SnippetForm()

    return render(request, 'vault/snippet_form.html', {
        'form': form,
        'titulo_pagina': 'Crear nuevo snippet',
        'texto_boton': 'Guardar snippet'
    })


def snippet_update(request, pk):
    # CRUD UPDATE: carga el registro actual y guarda cambios si el formulario es válido.
    snippet = get_object_or_404(Snippet, pk=pk)

    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            snippet = form.save()
            return redirect('snippet_detail', pk=snippet.pk)
    else:
        # FORMULARIO PRECARGADO: reutiliza la misma plantilla pero con datos existentes.
        form = SnippetForm(instance=snippet)

    return render(request, 'vault/snippet_form.html', {
        'form': form,
        'titulo_pagina': 'Editar snippet',
        'texto_boton': 'Actualizar snippet'
    })


def snippet_delete(request, pk):
    # CRUD DELETE: pide confirmación y elimina el registro solo mediante POST.
    snippet = get_object_or_404(Snippet, pk=pk)

    if request.method == 'POST':
        snippet.delete()
        return redirect('snippet_list')

    return render(request, 'vault/snippet_confirm_delete.html', {'snippet': snippet})
