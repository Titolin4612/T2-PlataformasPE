from django.shortcuts import get_object_or_404, redirect, render
from .forms import SnippetForm
from .models import Snippet


def snippet_list(request):
    snippets = Snippet.objects.all()
    return render(request, 'vault/snippet_list.html', {'snippets': snippets})


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
