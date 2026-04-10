from django.db import models


# MODELO PRINCIPAL: representa cada fragmento de código o comando guardado en la biblioteca.
class Snippet(models.Model):
    # CATÁLOGO DE LENGUAJES: opciones visibles y persistidas para clasificar snippets.
    LENGUAJES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('bash', 'Bash'),
        ('sql', 'SQL'),
        ('django', 'Django'),
        ('git', 'Git'),
        ('docker', 'Docker'),
        ('regex', 'Regex'),
        ('json', 'JSON'),
        ('yaml', 'YAML'),
    ]

    # CATÁLOGO DE CATEGORÍAS: agrupa los snippets por área funcional del proyecto o trabajo técnico.
    CATEGORIAS = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('database', 'Base de datos'),
        ('devops', 'DevOps'),
        ('utils', 'Utilidades'),
    ]

    # CAMPOS DEL MODELO: contienen la información que alimenta el CRUD y el listado público.
    titulo = models.CharField(max_length=120)
    lenguaje = models.CharField(max_length=20, choices=LENGUAJES)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    descripcion = models.TextField()
    codigo = models.TextField()
    destacado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        # METADATOS DEL MODELO: orden por defecto y nombres legibles para admin y migraciones.
        ordering = ['-creado_en']
        verbose_name = 'Snippet'
        verbose_name_plural = 'Snippets'

    def __str__(self):
        # REPRESENTACIÓN HUMANA: facilita reconocer el registro en admin, shell y logs.
        return self.titulo
