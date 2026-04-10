#tests.py contiene pruebas unitarias para verificar que todo este funcionando bien.

from io import StringIO
from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from vault.models import Snippet


class SnippetListViewTests(TestCase):
    def create_snippet(self, **overrides):
        data = {
            "titulo": "Snippet base",
            "lenguaje": "python",
            "categoria": "backend",
            "descripcion": "Descripcion de prueba",
            "codigo": "print('hola')",
            "destacado": False,
        }
        data.update(overrides)
        return Snippet.objects.create(**data)

    def test_list_supports_filtering_and_sorting_via_query_params(self):
        self.create_snippet(titulo="Alpha API helper", lenguaje="python", categoria="backend")
        self.create_snippet(titulo="Zeta API helper", lenguaje="python", categoria="backend")
        self.create_snippet(titulo="Terminal cleanup", lenguaje="bash", categoria="utils")

        response = self.client.get(
            reverse("snippet_list"),
            {
                "language": "python",
                "category": "backend",
                "sort": "title_desc",
            },
        )

        snippets = list(response.context["snippets"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual([snippet.titulo for snippet in snippets], ["Zeta API helper", "Alpha API helper"])
        self.assertEqual(response.context["results_count"], 2)
        self.assertEqual(response.context["active_language"], "python")
        self.assertEqual(response.context["active_category"], "backend")
        self.assertEqual(response.context["active_sort"], "title_desc")
        self.assertTrue(response.context["filters_active"])

    def test_copy_button_is_rendered_in_list_and_detail(self):
        snippet = self.create_snippet(titulo="Copiar comando")

        list_response = self.client.get(reverse("snippet_list"))
        detail_response = self.client.get(reverse("snippet_detail", args=[snippet.pk]))

        self.assertContains(list_response, 'data-copy-button')
        self.assertContains(list_response, f'id="snippet-copy-source-{snippet.pk}"')
        self.assertContains(detail_response, 'data-copy-button')
        self.assertContains(detail_response, f'id="snippet-code-{snippet.pk}"')

    def test_list_defaults_to_newest_without_internal_panels(self):
        older = self.create_snippet(titulo="Snippet antiguo")
        Snippet.objects.filter(pk=older.pk).update(creado_en=timezone.now() - timedelta(days=2))
        self.create_snippet(titulo="Snippet reciente")

        response = self.client.get(reverse("snippet_list"))
        snippets = list(response.context["snippets"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(snippets[0].titulo, "Snippet reciente")
        self.assertEqual(response.context["active_sort"], "newest")
        self.assertEqual(response.context["results_count"], 2)


class SeedSnippetsCommandTests(TestCase):
    def test_seed_command_is_idempotent_and_covers_required_groups(self):
        output = StringIO()

        call_command("seed_snippets", stdout=output)
        first_count = Snippet.objects.count()
        call_command("seed_snippets", stdout=output)
        second_count = Snippet.objects.count()

        languages = set(Snippet.objects.values_list("lenguaje", flat=True))
        categories = set(Snippet.objects.values_list("categoria", flat=True))

        self.assertGreaterEqual(first_count, 12)
        self.assertEqual(first_count, second_count)
        self.assertTrue({"git", "bash", "python", "javascript", "sql", "django"}.issubset(languages))
        self.assertTrue({"backend", "frontend", "database", "devops", "utils"}.issubset(categories))

    def test_create_form_exposes_all_languages_present_in_seed(self):
        response = self.client.get(reverse("snippet_create"))

        self.assertEqual(response.status_code, 200)
        language_values = {value for value, _label in response.context["form"].fields["lenguaje"].choices}

        self.assertTrue(
            {"bash", "css", "django", "docker", "git", "html", "javascript", "json", "python", "regex", "sql", "yaml"}.issubset(language_values)
        )
