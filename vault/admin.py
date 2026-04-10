from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Count
from urllib.parse import urlencode

from .models import Snippet


LANGUAGE_LABELS = dict(Snippet.LENGUAJES)


class VaultAdminSite(AdminSite):
    site_header = 'Command Vault Admin'
    site_title = 'Command Vault Admin'
    index_title = 'Panel de administracion'
    enable_nav_sidebar = False
    index_template = 'vault/admin/index.html'
    login_template = 'vault/admin/login.html'
    app_index_template = 'vault/admin/app_index.html'

    def each_context(self, request):
        context = super().each_context(request)
        snippets = Snippet.objects.order_by('-creado_en')
        top_languages = (
            snippets.values('lenguaje')
            .annotate(total=Count('pk'))
            .order_by('-total', 'lenguaje')[:4]
        )

        context['admin_dashboard'] = {
            'snippet_count': snippets.count(),
            'featured_count': snippets.filter(destacado=True).count(),
            'language_count': snippets.values('lenguaje').distinct().count(),
            'category_count': snippets.values('categoria').distinct().count(),
            'latest_snippets': snippets[:4],
            'top_languages': [
                {
                    'label': LANGUAGE_LABELS.get(item['lenguaje'], item['lenguaje']),
                    'total': item['total'],
                }
                for item in top_languages
            ],
        }
        return context


vault_admin_site = VaultAdminSite(name='admin')


@admin.register(Snippet, site=vault_admin_site)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'lenguaje_badge', 'categoria_badge', 'destacado', 'creado_en')
    ordering = ('-creado_en',)
    list_per_page = 100
    search_fields = ('titulo', 'descripcion', 'codigo')
    search_help_text = 'Busca por titulo, descripcion o contenido del codigo.'
    list_filter = ('lenguaje', 'categoria', 'destacado')
    readonly_fields = (
        'titulo',
        'lenguaje',
        'categoria',
        'descripcion',
        'codigo',
        'destacado',
        'creado_en',
        'actualizado_en',
    )
    actions = None
    change_list_template = 'vault/admin/snippets/change_list.html'
    change_form_template = 'vault/admin/snippets/change_form.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        if not hasattr(response, 'context_data'):
            return response

        cl = response.context_data.get('cl')
        if cl is None:
            return response

        search_query = request.GET.get('q', '')
        selected_filters = {
            'lenguaje': request.GET.get('lenguaje', ''),
            'categoria': request.GET.get('categoria', ''),
            'destacado__exact': request.GET.get('destacado__exact', ''),
        }

        response.context_data['search_hidden_inputs'] = [
            (key, value)
            for key, value in request.GET.items()
            if key not in {'q', 'p'} and value
        ]
        response.context_data['filter_sections'] = [
            self._build_filter_section(
                request.path,
                'Lenguajes',
                'lenguaje',
                Snippet.LENGUAJES,
                search_query,
                selected_filters,
            ),
            self._build_filter_section(
                request.path,
                'Categorias',
                'categoria',
                Snippet.CATEGORIAS,
                search_query,
                selected_filters,
            ),
            self._build_filter_section(
                request.path,
                'Estado',
                'destacado__exact',
                [('1', 'Destacados'), ('0', 'No destacados')],
                search_query,
                selected_filters,
            ),
        ]
        response.context_data['pagination_state'] = self._build_pagination_state(
            request.path,
            cl,
            search_query,
            selected_filters,
        )
        return response

    def _build_filter_section(self, base_url, title, param_name, options, search_query, selected_filters):
        params = {}
        if search_query:
            params['q'] = search_query
        for key, value in selected_filters.items():
            if key != param_name and value:
                params[key] = value

        items = [
            {
                'label': 'Todos',
                'selected': not selected_filters.get(param_name),
                'url': self._build_url(base_url, params),
            }
        ]
        for value, label in options:
            option_params = {**params, param_name: value}
            items.append(
                {
                    'label': label,
                    'selected': selected_filters.get(param_name) == value,
                    'url': self._build_url(base_url, option_params),
                }
            )

        return {'title': title, 'items': items}

    def _build_pagination_state(self, base_url, cl, search_query, selected_filters):
        params = {}
        if search_query:
            params['q'] = search_query
        for key, value in selected_filters.items():
            if value:
                params[key] = value

        current_page = cl.page_num + 1
        total_pages = cl.paginator.num_pages

        return {
            'current': current_page,
            'total': total_pages,
            'result_count': cl.result_count,
            'previous_url': self._build_page_url(base_url, params, cl.page_num - 1) if cl.page_num > 0 else None,
            'next_url': self._build_page_url(base_url, params, cl.page_num + 1)
            if cl.page_num + 1 < total_pages
            else None,
        }

    def _build_page_url(self, base_url, params, page_number):
        page_params = dict(params)
        if page_number > 0:
            page_params['p'] = page_number
        return self._build_url(base_url, page_params)

    def _build_url(self, base_url, params):
        query_string = urlencode(params)
        return f'{base_url}?{query_string}' if query_string else base_url

    @admin.display(description='Lenguaje')
    def lenguaje_badge(self, obj):
        return obj.get_lenguaje_display()

    @admin.display(description='Categoría')
    def categoria_badge(self, obj):
        return obj.get_categoria_display()

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_active and request.user.is_staff

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
