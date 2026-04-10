#views.py recibe las solicitudes del usuario a traves de urls.py y decide que hacer.

from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from .forms import SnippetForm
from .models import Snippet


SORT_OPTIONS = { #boton de ordenar para que el usuario elija como quiere ordenar.
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

#lista.
def snippet_list(request): #aqui es donde se muestra la lista de snippets, se filtra, ordena y se muestra lo necesario.
    base_queryset = Snippet.objects.all()
    snippets = base_queryset
    language_choices = dict(Snippet.LENGUAJES)
    category_choices = dict(Snippet.CATEGORIAS)

    active_language = request.GET.get('language', '').strip()
    active_category = request.GET.get('category', '').strip()
    active_sort = request.GET.get('sort', 'newest').strip()

    if active_language in language_choices: #filtrar por lenguaje
        snippets = snippets.filter(lenguaje=active_language)
    else:
        active_language = ''

    if active_category in category_choices: #filtrar por categoria
        snippets = snippets.filter(categoria=active_category)
    else:
        active_category = ''

    sort_config = SORT_OPTIONS.get(active_sort, SORT_OPTIONS['newest']) #ordenar por lo que el usuario elija, si no elige nada se ordena por lo mas nuevo.
    if active_sort not in SORT_OPTIONS:
        active_sort = 'newest'

    snippets = snippets.order_by(sort_config['order_by']) #aqui se aplica el orden elejido
    total_count = base_queryset.count()
    featured_count = base_queryset.filter(destacado=True).count()
    top_languages = list( #aqui se obtiene los 3 lenguajes mas usados en los snippets, se cuenta cuantos snippets hay por cada lenguaje y se ordena de mayor a menor, si hay empate se ordena alfabeticamente.
        base_queryset.values('lenguaje')
        .annotate(total=Count('id'))
        .order_by('-total', 'lenguaje')[:3]
    )

    for item in top_languages:
        item['label'] = language_choices.get(item['lenguaje'], item['lenguaje'])

    context = { #crea el contexto que se le va a pasar al template.
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
    return render(request, 'vault/snippet_list.html', context) #muestra el template(resultado) con el contexto que se le dio.

#detalle.
def snippet_detail(request, pk): #aqui se muestra el detalle de un snippet especifico
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, 'vault/snippet_detail.html', {'snippet': snippet}) #muestra el template de detalle con el snippet que se le dio.

#crear.
def snippet_create(request): #aqui se crea un nuevo snippet.
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

#editar.
def snippet_update(request, pk): #aqui se edita un snippet existente.
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

#eliminar.
def snippet_delete(request, pk): #aqui se elimina un snippet existente, se muestra una confirmacion antes de eliminarlo.
    snippet = get_object_or_404(Snippet, pk=pk)

    if request.method == 'POST':
        snippet.delete()
        return redirect('snippet_list')

    return render(request, 'vault/snippet_confirm_delete.html', {'snippet': snippet}) #muestra el template de confirmacion para eliminar el snippet.
