from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from .forms import SnippetForm
from .models import Snippet


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
    base_queryset = Snippet.objects.all()
    snippets = base_queryset
    language_choices = dict(Snippet.LENGUAJES)
    category_choices = dict(Snippet.CATEGORIAS)

    active_language = request.GET.get('language', '').strip()
    active_category = request.GET.get('category', '').strip()
    active_sort = request.GET.get('sort', 'newest').strip()

    if active_language in language_choices:
        snippets = snippets.filter(lenguaje=active_language)
    else:
        active_language = ''

    if active_category in category_choices:
        snippets = snippets.filter(categoria=active_category)
    else:
        active_category = ''

    sort_config = SORT_OPTIONS.get(active_sort, SORT_OPTIONS['newest'])
    if active_sort not in SORT_OPTIONS:
        active_sort = 'newest'

    snippets = snippets.order_by(sort_config['order_by'])
    total_count = base_queryset.count()
    featured_count = base_queryset.filter(destacado=True).count()
    top_languages = list(
        base_queryset.values('lenguaje')
        .annotate(total=Count('id'))
        .order_by('-total', 'lenguaje')[:3]
    )

    for item in top_languages:
        item['label'] = language_choices.get(item['lenguaje'], item['lenguaje'])

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
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, 'vault/snippet_detail.html', {'snippet': snippet})


def snippet_create(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save()
            return redirect('snippet_detail', pk=snippet.pk)
    else:
        form = SnippetForm()

    return render(request, 'vault/snippet_form.html', {
        'form': form,
        'titulo_pagina': 'Crear nuevo snippet',
        'texto_boton': 'Guardar snippet'
    })


def snippet_update(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)

    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            snippet = form.save()
            return redirect('snippet_detail', pk=snippet.pk)
    else:
        form = SnippetForm(instance=snippet)

    return render(request, 'vault/snippet_form.html', {
        'form': form,
        'titulo_pagina': 'Editar snippet',
        'texto_boton': 'Actualizar snippet'
    })


def snippet_delete(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)

    if request.method == 'POST':
        snippet.delete()
        return redirect('snippet_list')

    return render(request, 'vault/snippet_confirm_delete.html', {'snippet': snippet})
