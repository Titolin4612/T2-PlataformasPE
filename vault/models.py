from django.db import models


class Snippet(models.Model):
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

    CATEGORIAS = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('database', 'Base de datos'),
        ('devops', 'DevOps'),
        ('utils', 'Utilidades'),
    ]

    titulo = models.CharField(max_length=120)
    lenguaje = models.CharField(max_length=20, choices=LENGUAJES)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    descripcion = models.TextField()
    codigo = models.TextField()
    destacado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado_en']
        verbose_name = 'Snippet'
        verbose_name_plural = 'Snippets'

    def __str__(self):
        return self.titulo
