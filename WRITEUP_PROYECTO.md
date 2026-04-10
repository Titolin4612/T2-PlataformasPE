# Writeup Completo del Proyecto `Command Vault`

## 1. Objetivo de este documento

Este documento explica en detalle como funciona el proyecto, como esta construido, como se conecta con SQLite, cual es el flujo completo de una peticion web, que responsabilidad tiene cada archivo y que observaciones tecnicas importantes existen en el estado actual del repositorio.

La idea no es solo describir "que hace", sino dejar una documentacion suficientemente completa para:

- Entender la arquitectura del proyecto de principio a fin.
- Poder explicar el sistema en una sustentacion.
- Saber donde tocar el codigo si se quiere extender.
- Detectar decisiones de diseno, limitaciones y posibles mejoras.

---

## 2. Resumen ejecutivo

`Command Vault` es una aplicacion web hecha con Django para guardar, listar, filtrar, consultar, crear, editar y eliminar snippets de codigo o comandos tecnicos.

Su arquitectura es la clasica de Django:

1. El navegador hace una peticion HTTP.
2. Django resuelve la URL.
3. Una vista procesa la solicitud.
4. La vista consulta o modifica el modelo `Snippet` usando el ORM de Django.
5. El ORM traduce esas operaciones a SQL sobre SQLite.
6. La vista renderiza un template HTML y se lo devuelve al navegador.
7. Un pequeno archivo JavaScript agrega la funcionalidad de copiar codigo al portapapeles.

No es una SPA, no usa React, no usa API REST y no usa JavaScript complejo para renderizar la interfaz. Es una aplicacion renderizada en servidor con templates de Django.

---

## 3. Tecnologias y stack

### 3.1 Backend

- Python
- Django
- ORM de Django
- SQLite

### 3.2 Frontend

- Django Templates
- Tailwind CSS por CDN
- Google Fonts
- JavaScript vanilla

### 3.3 Persistencia

- Archivo local `db.sqlite3`

### 3.4 Dependencias declaradas

En `requirements.txt` aparecen:

- `Django==4.2.7`
- `asgiref==3.11.1`
- `sqlparse==0.5.5`

`asgiref` y `sqlparse` son dependencias de soporte que Django necesita internamente.

---

## 4. Estructura general del repositorio

La estructura importante del proyecto es esta:

```text
T2-PlataformasPE/
├── .venv/
├── venv/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── vault/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── management/
│   │   └── commands/
│   │       └── seed_snippets.py
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── 0002_alter_snippet_lenguaje.py
│   ├── static/
│   │   └── vault/
│   │       ├── app.css
│   │       └── app.js
│   └── templates/
│       └── vault/
│           ├── base.html
│           ├── snippet_confirm_delete.html
│           ├── snippet_detail.html
│           ├── snippet_form.html
│           └── snippet_list.html
├── db.sqlite3
├── manage.py
├── requirements.txt
└── WRITEUP_PROYECTO.md
```

### 4.1 Que significa cada parte

- `manage.py`: punto de entrada para ejecutar comandos de Django.
- `config/`: configuracion global del proyecto.
- `vault/`: aplicacion principal donde vive casi toda la logica de negocio.
- `db.sqlite3`: base de datos local.
- `requirements.txt`: dependencias Python.
- `.venv/` y `venv/`: entornos virtuales.

---

## 5. Arquitectura conceptual

La arquitectura del proyecto se puede entender asi:

```text
Usuario/Navegador
        |
        v
      URL
        |
        v
config/urls.py
        |
        v
vault/urls.py
        |
        v
    views.py
   /       \
  v         v
forms.py   models.py
              |
              v
       ORM de Django
              |
              v
         SQLite (db.sqlite3)
              |
              v
      resultado en Python
              |
              v
 templates/*.html
              |
              v
HTML renderizado al navegador
              |
              v
 app.js agrega copia al portapapeles
```

### 5.1 Idea clave de arquitectura

La logica principal esta del lado del servidor. Django no solo guarda datos; tambien:

- valida formularios,
- resuelve rutas,
- consulta la base,
- renderiza HTML,
- protege formularios con CSRF,
- administra sesiones y usuarios si se necesita,
- expone un panel admin listo para usar.

---

## 6. Punto de entrada y arranque del proyecto

### 6.1 `manage.py`

`manage.py` es el archivo con el que normalmente se arranca el proyecto. Su trabajo es:

- establecer la variable de entorno `DJANGO_SETTINGS_MODULE` apuntando a `config.settings`,
- cargar Django,
- reenviar los comandos recibidos desde consola a `execute_from_command_line`.

Ejemplos de uso:

```bash
./.venv/bin/python manage.py runserver
./.venv/bin/python manage.py migrate
./.venv/bin/python manage.py createsuperuser
./.venv/bin/python manage.py seed_snippets
./.venv/bin/python manage.py test vault
```

### 6.2 `config/settings.py`

Este es el archivo mas importante de configuracion global. Define:

- apps instaladas,
- middlewares,
- templates,
- base de datos,
- timezone,
- idioma,
- archivos estaticos,
- tipo por defecto de llave primaria.

### 6.3 `config/urls.py`

Este archivo enruta dos cosas:

- `/admin/` al panel de administracion de Django.
- `/` a las URLs de la app `vault`.

Eso significa que la aplicacion funcional para el usuario final vive completamente dentro de `vault`.

### 6.4 `config/wsgi.py` y `config/asgi.py`

Estos archivos exponen la aplicacion para servidores compatibles con:

- WSGI
- ASGI

En desarrollo normalmente no se tocan. Existen para que Django pueda ser desplegado en distintos entornos de produccion.

---

## 7. Configuracion global detallada

### 7.1 `BASE_DIR`

`BASE_DIR` apunta a la carpeta raiz del proyecto. Se usa para construir rutas absolutas internas, por ejemplo la ubicacion de la base de datos.

### 7.2 `INSTALLED_APPS`

Apps registradas:

- `django.contrib.admin`
- `django.contrib.auth`
- `django.contrib.contenttypes`
- `django.contrib.sessions`
- `django.contrib.messages`
- `django.contrib.staticfiles`
- `vault`

### 7.3 Que aporta cada app builtin

- `admin`: panel administrativo.
- `auth`: usuarios, grupos, permisos.
- `contenttypes`: soporte interno para asociar modelos y permisos.
- `sessions`: sesiones de usuario.
- `messages`: mensajes flash.
- `staticfiles`: manejo de archivos estaticos.

### 7.4 `MIDDLEWARE`

Middlewares activos:

- seguridad base,
- sesiones,
- procesamiento comun de peticiones,
- proteccion CSRF,
- autenticacion,
- mensajes,
- proteccion contra clickjacking.

Aunque la app publica no usa login para CRUD, Django igual trae la infraestructura lista.

### 7.5 Templates

Configuracion clave:

- `APP_DIRS = True`: Django buscara templates dentro de `templates/` de cada app.
- `DIRS = []`: no hay una carpeta global adicional de templates.

Eso significa que los templates de este proyecto viven dentro de `vault/templates/vault/`.

### 7.6 Base de datos

La app usa:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Esto conecta Django con un archivo SQLite llamado `db.sqlite3` en la raiz del proyecto.

### 7.7 Internacionalizacion

- `LANGUAGE_CODE = 'es-co'`
- `TIME_ZONE = 'America/Bogota'`
- `USE_I18N = True`
- `USE_TZ = True`

Consecuencia:

- la app esta pensada para contexto colombiano/espanol,
- Django trabaja con soporte de zonas horarias,
- las fechas se muestran formateadas en templates segun filtros de fecha.

### 7.8 Archivos estaticos

- `STATIC_URL = 'static/'`

No hay configuracion avanzada de `STATIC_ROOT` ni `STATICFILES_DIRS`, porque el proyecto parece pensado principalmente para desarrollo local.

### 7.9 `DEFAULT_AUTO_FIELD`

Se usa `BigAutoField`, es decir, IDs enteros grandes autoincrementales por defecto.

---

## 8. Como se conecta el proyecto con SQLite

Esta es una de las preguntas mas importantes de la sustentacion.

### 8.1 Respuesta corta

El proyecto se conecta a SQLite a traves del ORM de Django, configurando el backend `django.db.backends.sqlite3` en `config/settings.py`. No existe una conexion manual con `sqlite3.connect()` en el codigo del proyecto.

### 8.2 Respuesta tecnica completa

El flujo real es este:

1. Django arranca y lee `config/settings.py`.
2. Ve que la base configurada es SQLite.
3. Cada vez que el codigo usa `Snippet.objects...`, Django usa su ORM.
4. El ORM traduce esas operaciones Python a SQL.
5. Ese SQL se ejecuta sobre `db.sqlite3`.
6. Los resultados vuelven como objetos `Snippet`.

### 8.3 Donde esta la configuracion exacta

La configuracion esta en `config/settings.py`, en el bloque `DATABASES`.

### 8.4 Como se creo la tabla principal

La tabla `vault_snippet` no se creo a mano en SQLite. Se creo con migraciones de Django:

- `vault/migrations/0001_initial.py`
- `vault/migrations/0002_alter_snippet_lenguaje.py`

### 8.5 Tabla principal observada en la base

El esquema real observado de la tabla principal es:

```sql
CREATE TABLE "vault_snippet" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "titulo" varchar(120) NOT NULL,
  "lenguaje" varchar(20) NOT NULL,
  "categoria" varchar(20) NOT NULL,
  "descripcion" text NOT NULL,
  "codigo" text NOT NULL,
  "destacado" bool NOT NULL,
  "creado_en" datetime NOT NULL,
  "actualizado_en" datetime NOT NULL
);
```

### 8.6 Tablas existentes en la base

Ademas de `vault_snippet`, SQLite contiene tablas propias de Django:

- `auth_group`
- `auth_group_permissions`
- `auth_permission`
- `auth_user`
- `auth_user_groups`
- `auth_user_user_permissions`
- `django_admin_log`
- `django_content_type`
- `django_migrations`
- `django_session`

### 8.7 Que guarda cada grupo de tablas

- `vault_snippet`: datos funcionales de la aplicacion.
- `django_migrations`: historial de migraciones aplicadas.
- `auth_*`: usuarios, grupos y permisos.
- `django_session`: sesiones.
- `django_admin_log`: acciones realizadas en admin.
- `django_content_type`: metadatos internos de modelos.

### 8.8 Como se traduce el ORM a SQL

Ejemplos conceptuales:

- `Snippet.objects.all()` -> `SELECT * FROM vault_snippet`
- `Snippet.objects.filter(lenguaje='python')` -> `SELECT ... WHERE lenguaje='python'`
- `form.save()` en create -> `INSERT INTO vault_snippet (...) VALUES (...)`
- `form.save()` en update -> `UPDATE vault_snippet SET ... WHERE id=...`
- `snippet.delete()` -> `DELETE FROM vault_snippet WHERE id=...`

El desarrollador trabaja con Python; Django hace el puente hacia SQL.

### 8.9 Porque usar SQLite aqui

Ventajas en este proyecto:

- simple de configurar,
- no requiere servidor aparte,
- ideal para un proyecto pequeno o academico,
- el archivo de base vive dentro del repo.

Desventajas si el sistema creciera:

- menor escalabilidad,
- mas limitado en concurrencia,
- no ideal para trafico alto,
- menos flexible para despliegues distribuidos.

---

## 9. Modelo de dominio: `Snippet`

El modelo central es `Snippet`, definido en `vault/models.py`.

### 9.1 Campos

#### `titulo`

- Tipo: `CharField`
- Longitud maxima: 120
- Proposito: nombre descriptivo del snippet

#### `lenguaje`

- Tipo: `CharField`
- Longitud maxima: 20
- Usa `choices`
- Proposito: clasificar el snippet por tecnologia o lenguaje

Valores permitidos:

- python
- javascript
- html
- css
- bash
- sql
- django
- git
- docker
- regex
- json
- yaml

#### `categoria`

- Tipo: `CharField`
- Longitud maxima: 20
- Usa `choices`

Categorias:

- backend
- frontend
- database
- devops
- utils

#### `descripcion`

- Tipo: `TextField`
- Proposito: explicar que hace el snippet

#### `codigo`

- Tipo: `TextField`
- Proposito: guardar el fragmento de codigo, comando o texto tecnico

#### `destacado`

- Tipo: `BooleanField`
- Default: `False`
- Proposito: marcar snippets importantes

#### `creado_en`

- Tipo: `DateTimeField(auto_now_add=True)`
- Se asigna automaticamente al crear

#### `actualizado_en`

- Tipo: `DateTimeField(auto_now=True)`
- Se actualiza automaticamente en cada modificacion

### 9.2 Reglas adicionales del modelo

Dentro de `Meta`:

- `ordering = ['-creado_en']`
- `verbose_name = 'Snippet'`
- `verbose_name_plural = 'Snippets'`

Esto significa que por defecto los snippets salen ordenados del mas reciente al mas antiguo.

### 9.3 Metodo `__str__`

Devuelve el `titulo`, lo cual mejora:

- el admin,
- el shell,
- el debug,
- la lectura de objetos en logs o consola.

### 9.4 Observacion importante

El `titulo` no es unico a nivel de base de datos. Eso implica que:

- desde formularios normales se podrian crear dos snippets con el mismo titulo,
- el comando `seed_snippets` evita duplicados usando `update_or_create` por titulo,
- pero esa regla no esta reforzada por una restriccion `unique=True`.

---

## 10. Formularios: `SnippetForm`

El formulario principal vive en `vault/forms.py`.

### 10.1 Tipo de formulario

Es un `ModelForm`.

Esto significa que Django genera automaticamente los campos del formulario a partir del modelo `Snippet`.

### 10.2 Campos incluidos

El formulario expone:

- `titulo`
- `lenguaje`
- `categoria`
- `descripcion`
- `codigo`
- `destacado`

### 10.3 Ventajas de usar `ModelForm`

- menos codigo manual,
- validacion integrada,
- coherencia con el modelo,
- guardado simple con `form.save()`.

### 10.4 Personalizacion visual

El formulario define widgets con clases CSS utilitarias para:

- inputs de texto,
- `select`,
- `textarea`,
- checkbox.

Eso hace que el formulario ya salga estilizado sin tener que escribir HTML complejo por campo.

### 10.5 Validacion

Aunque no hay validaciones personalizadas escritas a mano, Django ya valida:

- que existan campos requeridos,
- que el valor de `lenguaje` este dentro de los `choices`,
- que `categoria` este dentro de sus `choices`,
- que el largo del titulo no exceda 120,
- que el tipo de datos sea correcto.

---

## 11. Rutas del proyecto

Las rutas de la app estan en `vault/urls.py`.

### 11.1 Mapa de rutas

- `/` -> lista de snippets
- `/snippet/<int:pk>/` -> detalle de un snippet
- `/crear/` -> formulario de creacion
- `/editar/<int:pk>/` -> formulario de edicion
- `/eliminar/<int:pk>/` -> confirmacion de borrado

### 11.2 Nombres de ruta

Cada URL tiene nombre:

- `snippet_list`
- `snippet_detail`
- `snippet_create`
- `snippet_update`
- `snippet_delete`

Esto permite usar:

- `{% url 'snippet_list' %}` en templates
- `redirect('snippet_detail', pk=...)` en vistas
- `reverse('snippet_list')` en tests

Esa es la manera recomendada en Django porque evita hardcodear rutas.

---

## 12. Vistas: logica completa del sistema

Las vistas estan en `vault/views.py`. Aqui vive el comportamiento del CRUD.

## 12.1 `snippet_list(request)`

Esta es la vista mas rica del proyecto.

### 12.1.1 Objetivo

- listar snippets,
- aplicar filtros,
- aplicar orden,
- calcular estadisticas,
- enviar contexto al template principal.

### 12.1.2 Flujo interno paso a paso

1. Parte de `Snippet.objects.all()`.
2. Convierte los choices a diccionarios para validarlos facilmente.
3. Lee query params:
   - `language`
   - `category`
   - `sort`
4. Si `language` es valido, filtra por `lenguaje`.
5. Si `category` es valido, filtra por `categoria`.
6. Si el criterio de orden existe, usa el `order_by` correspondiente.
7. Calcula:
   - total de snippets,
   - total de destacados,
   - top 3 lenguajes por cantidad.
8. Construye un `context` grande.
9. Renderiza `vault/snippet_list.html`.

### 12.1.3 Parametros GET soportados

- `language`
- `category`
- `sort`

Ejemplo:

```text
/?language=python&category=backend&sort=title_desc
```

### 12.1.4 Como valida los filtros

La vista no acepta cualquier string ciegamente. Primero revisa si el valor existe en los choices permitidos.

Ejemplo conceptual:

- si `language=python`, filtra
- si `language=algo_invalido`, ignora el filtro

Eso evita estados incoherentes y reduce errores.

### 12.1.5 Opciones de orden

- `newest`: mas recientes
- `oldest`: mas antiguos
- `title_asc`: titulo A-Z
- `title_desc`: titulo Z-A

### 12.1.6 Estadisticas generadas

La vista arma informacion adicional para enriquecer la portada:

- `total_count`
- `featured_count`
- `results_count`
- `top_languages`

El `top_languages` se calcula con agregacion:

```python
base_queryset.values('lenguaje').annotate(total=Count('id'))
```

Eso en terminos conceptuales es un `GROUP BY lenguaje`.

### 12.1.7 Datos enviados al template

El `context` incluye:

- resultados,
- choices,
- filtros activos,
- etiquetas amigables del filtro,
- conteos,
- top lenguajes,
- estado del orden actual.

### 12.1.8 Valor tecnico de esta vista

Esta vista mezcla:

- lectura de query params,
- validacion,
- consultas ORM,
- agregaciones,
- presentacion.

Es la vista que mejor representa la logica del sistema.

---

## 12.2 `snippet_detail(request, pk)`

### 12.2.1 Objetivo

Mostrar un snippet especifico.

### 12.2.2 Funcionamiento

- usa `get_object_or_404(Snippet, pk=pk)`
- si existe, renderiza el template detalle
- si no existe, Django responde 404

### 12.2.3 Porque es buena practica

`get_object_or_404` evita:

- tener que manejar `try/except` manuales,
- devolver errores silenciosos,
- mostrar pantallas inconsistentes.

---

## 12.3 `snippet_create(request)`

### 12.3.1 Objetivo

Crear un nuevo snippet.

### 12.3.2 Flujo GET

Si la peticion es `GET`:

- crea `form = SnippetForm()`
- renderiza el formulario vacio

### 12.3.3 Flujo POST

Si la peticion es `POST`:

1. construye `SnippetForm(request.POST)`
2. valida con `form.is_valid()`
3. guarda con `form.save()`
4. redirige al detalle del snippet creado

### 12.3.4 Que pasa en la base

Cuando `form.save()` se ejecuta:

- Django crea un objeto `Snippet`
- genera el `INSERT` en SQLite
- rellena `creado_en` y `actualizado_en`
- devuelve la instancia ya persistida

### 12.3.5 Beneficio de redirigir al detalle

Despues de crear, el usuario queda viendo el resultado final y no reenvia el formulario si recarga.

---

## 12.4 `snippet_update(request, pk)`

### 12.4.1 Objetivo

Editar un snippet existente.

### 12.4.2 Diferencia frente a create

La diferencia clave es que se pasa `instance=snippet` al formulario.

Esto hace que Django:

- precargue los valores actuales,
- y al guardar haga `UPDATE` en vez de `INSERT`.

### 12.4.3 Flujo

1. busca el snippet con `get_object_or_404`
2. si es `GET`, muestra el formulario lleno
3. si es `POST`, valida cambios
4. si el formulario es valido, hace `form.save()`
5. redirige al detalle

### 12.4.4 Campo que cambia automaticamente

`actualizado_en` se refresca por `auto_now=True`.

---

## 12.5 `snippet_delete(request, pk)`

### 12.5.1 Objetivo

Eliminar un snippet.

### 12.5.2 Patron usado

No borra directamente al entrar por URL. Primero:

- busca el objeto,
- muestra pantalla de confirmacion,
- solo si llega un `POST` ejecuta `delete()`.

### 12.5.3 Porque es correcto

Evita borrados accidentales por:

- enlaces,
- recargas,
- clicks involuntarios,
- acceso directo sin confirmacion.

### 12.5.4 Resultado

Tras borrar:

- elimina el registro de SQLite,
- redirige a la lista principal.

---

## 13. Templates: capa de presentacion

Los templates estan en `vault/templates/vault/`.

Este proyecto usa herencia de templates, una de las caracteristicas mas importantes de Django.

## 13.1 `base.html`

Es la plantilla base de toda la app.

### 13.1.1 Responsabilidades

- define el `doctype` y estructura HTML general,
- carga Google Fonts,
- carga Tailwind por CDN,
- define configuracion de Tailwind embebida,
- construye el fondo general,
- pinta la barra superior,
- incluye el boton "Nuevo snippet",
- define el bloque `{% block content %}`,
- carga `app.js`.

### 13.1.2 Implicacion importante

Como los otros templates hacen:

```django
{% extends 'vault/base.html' %}
```

todos heredan la misma cabecera, estilo global y layout principal.

### 13.1.3 Tailwind por CDN

La interfaz depende de:

```html
<script src="https://cdn.tailwindcss.com"></script>
```

Esto es comodo en desarrollo, pero implica dependencia de internet para el estilo.

## 13.2 `snippet_list.html`

Es la vista principal de la aplicacion.

### 13.2.1 Partes visuales

- hero principal de bienvenida,
- tarjetas de metricas,
- panel "que puedes hacer aqui",
- panel de top lenguajes,
- formulario de filtros,
- chips que muestran filtros activos,
- grid de snippets,
- estados vacios.

### 13.2.2 Como muestra un snippet

Cada tarjeta enseña:

- lenguaje,
- categoria,
- marca de destacado,
- titulo,
- descripcion truncada,
- fragmento de codigo truncado,
- fecha de creacion,
- boton de copiar,
- boton "Ver detalle".

### 13.2.3 Detalles interesantes

- usa `snippet.get_lenguaje_display` para mostrar el label humano del choice.
- usa `snippet.get_categoria_display` para lo mismo en categoria.
- usa `truncatechars` para no romper el diseno con textos muy largos.
- si el snippet es destacado, cambia el estilo visual.

### 13.2.4 Estados posibles

La plantilla maneja tres escenarios:

1. Hay snippets para mostrar.
2. Hay snippets en la base, pero no coinciden con el filtro actual.
3. No hay snippets todavia.

Eso mejora mucho la UX.

## 13.3 `snippet_detail.html`

Muestra un snippet completo.

### 13.3.1 Que incluye

- badges de lenguaje/categoria/destacado,
- titulo completo,
- descripcion completa,
- bloque de codigo completo,
- boton copiar,
- fecha de creacion,
- fecha de actualizacion,
- botones editar y eliminar,
- enlace para volver a la lista.

### 13.3.2 Diferencia frente a la lista

En la lista se muestra un resumen. Aqui se muestra el contenido completo.

## 13.4 `snippet_form.html`

Se reutiliza tanto para crear como para editar.

### 13.4.1 Beneficio

Un solo template sirve para dos casos de uso porque la vista le pasa:

- `titulo_pagina`
- `texto_boton`
- `form`

### 13.4.2 Proteccion CSRF

Incluye:

```django
{% csrf_token %}
```

Esto es obligatorio en formularios `POST` en Django y protege contra ataques CSRF.

## 13.5 `snippet_confirm_delete.html`

Pantalla de confirmacion de borrado.

### 13.5.1 Buenas practicas presentes

- solicita confirmacion explicita,
- usa `POST`,
- advierte que la accion no se puede deshacer.

---

## 14. JavaScript: comportamiento del cliente

El archivo importante es `vault/static/vault/app.js`.

### 14.1 Objetivo

Permitir copiar el contenido de un snippet al portapapeles.

### 14.2 Funcion `copySnippetText(text)`

Esta funcion intenta copiar de dos maneras:

1. Si existe `navigator.clipboard` y el contexto es seguro, usa la API moderna.
2. Si no, crea un `textarea` temporal oculto y usa `document.execCommand('copy')` como fallback.

### 14.3 Flujo del evento

Cuando el DOM carga:

- busca todos los elementos con `data-copy-button`,
- obtiene el selector del origen desde `data-copy-source`,
- extrae el texto,
- intenta copiarlo,
- si funciona, cambia el boton a estado `Copiado`,
- si falla, lo cambia a estado `Error`,
- luego de 1.8 segundos lo devuelve al estado original.

### 14.4 Como se conecta con el HTML

En la lista:

- el boton apunta a un `textarea hidden` con el contenido completo del codigo.

En el detalle:

- el boton apunta al bloque `<pre>` completo.

### 14.5 Valor tecnico

Es un JavaScript pequeno, aislado y progresivo. No controla la app; solo mejora la experiencia de usuario.

---

## 15. CSS: archivo existente pero no usado

Existe un archivo `vault/static/vault/app.css`.

### 15.1 Observacion importante

Actualmente `base.html` no lo carga con una etiqueta `<link>`.

Eso sugiere una de estas posibilidades:

- es un archivo legado de una version anterior,
- fue creado como alternativa a Tailwind,
- o se dejo preparado pero nunca se conecto.

### 15.2 Conclusion practica

La interfaz real del proyecto hoy depende principalmente de:

- Tailwind por CDN,
- clases inline en los templates.

`app.css` no participa en el renderizado visible mientras no se enlace desde `base.html`.

---

## 16. Admin de Django

El admin esta configurado en `vault/admin.py`.

### 16.1 Que hace

Registra el modelo `Snippet` con:

- columnas visibles en lista,
- filtros,
- buscador.

### 16.2 Configuracion aplicada

- `list_display = ('titulo', 'lenguaje', 'categoria', 'destacado', 'creado_en')`
- `list_filter = ('lenguaje', 'categoria', 'destacado')`
- `search_fields = ('titulo', 'descripcion', 'codigo')`

### 16.3 Valor del admin

Permite administrar snippets sin programar un panel extra. Para un proyecto academico o pequeno esto es una gran ventaja porque Django ya resuelve:

- autenticacion,
- permisos,
- listado,
- formulario,
- filtros,
- edicion.

---

## 17. Configuracion minima de la app

`vault/apps.py` define `VaultConfig`.

### 17.1 Proposito

Registrar la aplicacion `vault` en Django.

### 17.2 Configuracion

- `default_auto_field = 'django.db.models.BigAutoField'`
- `name = 'vault'`

Es una configuracion minima, suficiente para que Django detecte correctamente la app.

---

## 18. Migraciones

Las migraciones son fundamentales para explicar como se construyo la base de datos.

## 18.1 `0001_initial.py`

Esta migracion crea el modelo `Snippet` y por tanto la tabla `vault_snippet`.

### 18.1.1 Que crea

- id
- titulo
- lenguaje
- categoria
- descripcion
- codigo
- destacado
- creado_en
- actualizado_en

Tambien define:

- nombre amigable del modelo,
- orden por defecto.

## 18.2 `0002_alter_snippet_lenguaje.py`

Esta migracion modifica el campo `lenguaje` para ampliar los choices disponibles e incluir:

- docker
- regex
- json
- yaml

### 18.2.1 Lectura importante

Esto muestra que el proyecto evoluciono. Primero habia menos lenguajes y despues se extendio la clasificacion.

## 18.3 Como se aplican

Con:

```bash
./.venv/bin/python manage.py migrate
```

### 18.3.1 Estado observado

Las migraciones actualmente aparecen aplicadas para:

- `admin`
- `auth`
- `contenttypes`
- `sessions`
- `vault`

---

## 19. Comando personalizado de carga de datos

El archivo `vault/management/commands/seed_snippets.py` define un comando custom de Django.

### 19.1 Objetivo

Poblar la base con snippets de ejemplo.

### 19.2 Como se ejecuta

```bash
./.venv/bin/python manage.py seed_snippets
```

### 19.3 Como funciona internamente

1. Define una lista grande `SAMPLE_SNIPPETS`.
2. Recorre cada item.
3. Usa `Snippet.objects.update_or_create(...)`.
4. Busca por `titulo`.
5. Si no existe, crea.
6. Si ya existe, actualiza sus campos.
7. Cuenta cuantos fueron creados y cuantos actualizados.
8. Imprime un resumen final.

### 19.4 Porque usa `@transaction.atomic`

La decoracion `@transaction.atomic` asegura que el proceso se ejecute como una transaccion. Si algo fallara a mitad del proceso, Django puede revertir el bloque para no dejar el seed a medias.

### 19.5 Que significa que sea idempotente

El comando es esencialmente idempotente porque:

- si lo ejecutas una vez, crea datos,
- si lo ejecutas de nuevo, no deberia duplicarlos,
- en lugar de duplicar, actualiza por titulo.

### 19.6 Tipos de snippets cargados

La semilla incluye contenidos de:

- Git
- Bash
- Python
- JavaScript
- Django
- SQL
- Docker
- Regex
- JSON
- YAML

Y categorias como:

- backend
- frontend
- database
- devops
- utils

### 19.7 Importante: el seed contiene contenido, no dependencias runtime

Algunos snippets mencionan tecnologias como `requests`, `bcrypt`, `pandas`, `postgres`, `redis`, etc. Eso no significa que el proyecto las use como librerias activas. Solo significa que el contenido guardado en la base habla sobre esas tecnologias.

---

## 20. Pruebas automatizadas

Las pruebas estan en `vault/tests.py`.

## 20.1 Tipo de pruebas

Son pruebas de Django con `TestCase`.

## 20.2 Casos cubiertos

### 20.2.1 Filtrado y ordenamiento de la lista

Verifica que:

- se apliquen `language`, `category` y `sort`,
- el orden de salida sea correcto,
- el contexto refleje filtros activos.

### 20.2.2 Render del boton de copiar

Verifica que:

- la lista contenga `data-copy-button`,
- el detalle contenga `data-copy-button`,
- existan las fuentes correctas para copiar el texto.

### 20.2.3 Orden por defecto

Verifica que:

- sin parametros de orden, la lista salga por mas recientes primero.

### 20.2.4 Idempotencia del seed

Verifica que:

- el comando `seed_snippets` no duplique registros al correrse dos veces,
- se cubran grupos y lenguajes esperados.

### 20.2.5 Lenguajes expuestos por el formulario

Verifica que el formulario permita todos los lenguajes esperados por la semilla.

## 20.3 Hallazgo real al ejecutar tests en este entorno

En esta maquina:

- `./.venv/bin/python manage.py check` funciona,
- pero `./.venv/bin/python manage.py test vault` falla.

### 20.3.1 Causa observada

Los errores estan relacionados con una incompatibilidad entre:

- Python `3.14.3` en `.venv`
- Django `4.2.7`

El fallo aparece durante el render instrumentado de templates en el cliente de pruebas de Django.

### 20.3.2 Conclusiones practicas

- El codigo del proyecto no necesariamente esta roto funcionalmente.
- El entorno de testing actual si presenta una incompatibilidad.
- Para dejar los tests estables probablemente habria que:
  - usar una version de Python soportada oficialmente por Django 4.2,
  - o actualizar Django a una version compatible con Python 3.14.

---

## 21. Flujo funcional completo por caso de uso

Aqui se explica el recorrido de cada operacion de negocio.

## 21.1 Caso 1: listar snippets

1. El usuario entra a `/`.
2. `config/urls.py` delega a `vault.urls`.
3. `vault.urls` envia a `snippet_list`.
4. La vista consulta la base con el ORM.
5. La vista construye el contexto.
6. Se renderiza `snippet_list.html`.
7. El navegador recibe HTML ya resuelto.

## 21.2 Caso 2: filtrar snippets

1. El usuario selecciona lenguaje/categoria/orden.
2. El formulario manda `GET`.
3. La URL queda con query params.
4. `snippet_list` lee esos parametros.
5. Valida si son choices permitidos.
6. Filtra con `.filter(...)`.
7. Ordena con `.order_by(...)`.
8. Renderiza los resultados filtrados.

## 21.3 Caso 3: crear snippet

1. El usuario entra a `/crear/`.
2. La vista muestra el formulario vacio.
3. El usuario completa los campos.
4. Se envia un `POST`.
5. Django valida el formulario.
6. Si es valido, guarda en SQLite.
7. Redirige al detalle del nuevo snippet.

## 21.4 Caso 4: editar snippet

1. El usuario entra a `/editar/<id>/`.
2. Django busca el snippet.
3. El formulario se precarga con los datos actuales.
4. El usuario modifica y envia.
5. Django valida.
6. Hace `UPDATE` en la base.
7. Redirige al detalle actualizado.

## 21.5 Caso 5: eliminar snippet

1. El usuario entra a `/eliminar/<id>/`.
2. Ve una pantalla de confirmacion.
3. Si confirma, el navegador manda `POST`.
4. Django ejecuta `delete()`.
5. Redirige a la lista.

## 21.6 Caso 6: copiar snippet

1. El usuario pulsa un boton "Copiar".
2. `app.js` detecta el click.
3. Toma el texto desde el elemento indicado.
4. Lo copia al portapapeles.
5. Cambia el estado visual del boton.

---

## 22. Estado actual observado de la base de datos

Esta seccion documenta una fotografia real de la base `db.sqlite3` en el estado actual del repositorio.

### 22.1 Conteo total

- `108` snippets en `vault_snippet`

### 22.2 Distribucion por lenguaje

- `git`: 28
- `bash`: 16
- `python`: 16
- `javascript`: 11
- `django`: 10
- `sql`: 10
- `css`: 6
- `html`: 4
- `regex`: 3
- `docker`: 2
- `json`: 1
- `yaml`: 1

### 22.3 Distribucion por categoria

- `utils`: 28
- `devops`: 27
- `backend`: 22
- `frontend`: 21
- `database`: 10

### 22.4 Lectura funcional

Esto confirma que:

- la base no esta vacia,
- el sistema ya tiene contenido suficiente para mostrar filtros y metricas,
- `git` es actualmente el lenguaje con mayor presencia,
- `utils` y `devops` dominan la clasificacion.

---

## 23. Decision de diseno de interfaz

Aunque el proyecto es Django server-side, la interfaz esta bastante trabajada visualmente.

### 23.1 Caracteristicas visuales

- fondo oscuro con gradientes,
- paneles translcidos,
- uso de tipografia `Space Grotesk` y `JetBrains Mono`,
- tarjetas con estados visuales,
- uso intensivo de Tailwind utility classes,
- feedback visual en el copiado.

### 23.2 Que no se usa

- no hay componentes React,
- no hay bundle de frontend,
- no hay `npm`,
- no hay sistema de estados cliente complejo,
- no hay CSS modular enlazado desde `app.css`.

### 23.3 Conclusion

La UI esta basada en HTML renderizado en servidor mas utilidades CSS declaradas en templates.

---

## 24. Observaciones tecnicas y hallazgos importantes

Esta es una seccion clave para una sustentacion madura. No solo describe lo bueno; tambien muestra lectura critica del proyecto.

## 24.1 Inconsistencia de versiones de Django

`requirements.txt` y `.venv` muestran `Django 4.2.7`, pero varios archivos contienen comentarios autogenerados que dicen `Django 5.2.13`.

Esto sugiere una de estas situaciones:

- el proyecto fue generado o modificado en otra maquina/version,
- se cambiaron archivos sin sincronizar la dependencia final,
- el comentario no refleja exactamente el runtime actual.

## 24.2 Dos entornos virtuales

Existen:

- `.venv`
- `venv`

### 24.2.1 Estado observado

- `.venv` funciona en esta maquina.
- `venv` parece provenir de otro entorno, incluso con referencias a una ruta de macOS.

### 24.2.2 Recomendacion practica

Para trabajar hoy en esta maquina, conviene usar `.venv`.

## 24.3 Tests fallando por entorno

Los tests no estan verdes en el entorno actual por incompatibilidad tecnica del stack usado para ejecutarlos.

## 24.4 `app.css` no conectado

Existe codigo CSS adicional no utilizado.

## 24.5 Seguridad y despliegue

El proyecto esta claramente en modo desarrollo:

- `DEBUG = True`
- `ALLOWED_HOSTS = []`
- `SECRET_KEY` hardcodeada en el repo

Esto esta bien para ambiente academico/local, pero no para produccion.

## 24.6 CRUD sin autenticacion

Actualmente cualquier usuario con acceso a la aplicacion puede:

- crear,
- editar,
- eliminar snippets

No hay restricciones de login sobre esas rutas publicas.

## 24.7 Sin paginacion ni busqueda textual

La lista filtra por lenguaje, categoria y orden, pero no por texto libre, y tampoco pagina resultados. Con 108 snippets sigue siendo manejable, pero a gran escala puede quedarse corto.

## 24.8 Sin restriccion unica de titulo

El seed trata el titulo como identificador logico, pero la base no lo fuerza como unico.

## 24.9 Dependencia de internet para estilo

Como Tailwind y Google Fonts vienen por CDN:

- si no hay internet, la UI puede verse mal o incompleta.

---

## 25. Como levantar el proyecto

## 25.1 Opcion recomendada en este repositorio

Usar `.venv`.

### 25.1.1 Verificacion rapida

```bash
./.venv/bin/python -V
./.venv/bin/python manage.py check
```

## 25.2 Comandos utiles

### Aplicar migraciones

```bash
./.venv/bin/python manage.py migrate
```

### Cargar datos de ejemplo

```bash
./.venv/bin/python manage.py seed_snippets
```

### Correr servidor local

```bash
./.venv/bin/python manage.py runserver
```

### Crear usuario admin

```bash
./.venv/bin/python manage.py createsuperuser
```

### Revisar migraciones

```bash
./.venv/bin/python manage.py showmigrations
```

## 25.3 URL esperada

En desarrollo, Django usualmente corre en:

```text
http://127.0.0.1:8000/
```

Y admin en:

```text
http://127.0.0.1:8000/admin/
```

---

## 26. Como defender este proyecto en una sustentacion

Esta seccion esta escrita pensando directamente en exposicion oral.

## 26.1 Explicacion corta de 30 segundos

"Este proyecto es una aplicacion web hecha con Django para guardar y administrar snippets de codigo. Usa un modelo principal llamado `Snippet`, persiste datos en SQLite mediante el ORM de Django y ofrece un CRUD completo con filtros por lenguaje, categoria y orden. La interfaz esta renderizada en servidor con templates de Django y tiene un pequeno JavaScript para copiar codigo al portapapeles."

## 26.2 Explicacion de 1 a 2 minutos

"La arquitectura sigue el flujo clasico de Django. El usuario entra por una URL, Django la resuelve y llama una vista. La vista consulta o actualiza el modelo `Snippet` usando el ORM, que a su vez traduce todo a SQL sobre una base SQLite local llamada `db.sqlite3`. Luego la vista arma un contexto y renderiza un template HTML. La interfaz principal muestra una biblioteca de snippets, estadisticas, filtros por lenguaje y categoria, y permite crear, editar, eliminar y copiar snippets. Adicionalmente, el proyecto incluye admin de Django, migraciones, pruebas automatizadas y un comando de seed para poblar datos de ejemplo sin duplicarlos."

## 26.3 Preguntas que probablemente te pueden hacer

### "Como se conectaron a SQLite?"

Respuesta:

"La conexion no se hizo manualmente. Se configuro en `settings.py` el backend `django.db.backends.sqlite3` apuntando al archivo `db.sqlite3`. Luego todas las operaciones se hacen con el ORM de Django, por ejemplo `Snippet.objects.all()`, `form.save()` o `snippet.delete()`."

### "Donde esta la logica principal?"

Respuesta:

"La logica funcional esta sobre todo en `vault/views.py`, porque ahi se procesan filtros, orden, consultas, creacion, edicion y eliminacion. El modelo define la estructura de datos y el formulario encapsula la validacion y el render de campos."

### "Que componentes tiene el sistema?"

Respuesta:

"Tiene configuracion global en `config`, una app principal `vault`, un modelo `Snippet`, formularios, vistas, templates, JavaScript para copiar, un admin, migraciones, pruebas y un comando de seed."

### "Por que usar Django y no otro enfoque?"

Respuesta:

"Porque para este tipo de aplicacion CRUD Django resuelve muy bien routing, ORM, formularios, templates, seguridad CSRF, panel admin y migraciones con muy poco codigo adicional."

### "Que mejora le harian?"

Respuesta:

"Autenticacion para proteger el CRUD, paginacion, busqueda por texto, consistencia de versiones de Django, estabilizacion del entorno de testing y limpieza del entorno virtual duplicado."

## 26.4 Forma recomendada de contar el flujo

Una buena secuencia para explicar es:

1. Que problema resuelve la app.
2. Que tecnologia principal usa.
3. Cual es el modelo de datos.
4. Como viaja una peticion desde URL hasta SQLite y de vuelta al HTML.
5. Que operaciones de usuario soporta.
6. Que puntos fuertes y limitaciones tiene.

---

## 27. Preguntas y respuestas tecnicas mas profundas

## 27.1 "Por que el formulario no escribe SQL?"

Porque Django abstrae la persistencia. `ModelForm` genera y valida datos; `form.save()` termina creando o actualizando la instancia del modelo, y el ORM se encarga del SQL real.

## 27.2 "Como sabe el template mostrar `Python` en vez de `python`?"

Porque el campo `lenguaje` usa `choices`. Django genera automaticamente el metodo `get_lenguaje_display()`, que devuelve la etiqueta humana del valor guardado.

## 27.3 "Como evita filtros invalidos?"

La vista compara los parametros con los `choices` definidos en el modelo. Si el valor no existe, lo descarta y limpia la variable.

## 27.4 "Como se calculan los lenguajes mas usados?"

Con una agregacion del ORM usando `Count`. Eso equivale a agrupar por lenguaje y contar registros.

## 27.5 "Por que el borrado usa POST y no GET?"

Porque borrar con GET es inseguro y rompe buenas practicas HTTP. Un enlace GET no deberia producir efectos destructivos.

## 27.6 "Que protege el formulario contra ataques?"

El token CSRF incluido con `{% csrf_token %}` y el middleware de CSRF de Django.

---

## 28. Posibles mejoras futuras

Si este proyecto evolucionara, las mejoras mas razonables serian:

- agregar autenticacion y permisos al CRUD publico,
- hacer `titulo` unico o agregar un slug,
- agregar busqueda textual por titulo/descripcion/codigo,
- agregar paginacion,
- mover Tailwind a un pipeline local en vez de CDN,
- decidir entre `.venv` y `venv` y dejar solo uno,
- unificar version de Django y Python compatibles,
- arreglar el entorno de tests,
- enlazar o eliminar `app.css`,
- agregar validaciones propias o normalizacion de datos,
- agregar exportacion/importacion de snippets,
- crear API REST si se quisiera un frontend desacoplado.

---

## 29. Conclusiones finales

`Command Vault` es un proyecto pequeno pero muy claro para explicar arquitectura web con Django. Tiene una estructura limpia, una unica entidad de negocio central, un CRUD completo y un uso correcto del ORM para persistencia con SQLite.

Sus puntos fuertes principales son:

- simplicidad estructural,
- buen uso del stack Django tradicional,
- interfaz cuidada,
- filtros utiles,
- comando de seed,
- admin,
- migraciones,
- pruebas.

Sus puntos debiles o areas de mejora son:

- entorno virtual duplicado,
- incompatibilidad actual de testing,
- inconsistencia de versiones de Django,
- ausencia de autenticacion en el CRUD publico,
- dependencia de CDN para el estilo,
- falta de paginacion/busqueda avanzada.

En una sustentacion, lo mas importante es transmitir que entiendes el recorrido completo:

`URL -> Vista -> ORM -> SQLite -> Template -> HTML -> JavaScript auxiliar`

Si explicas con claridad ese flujo y el rol del modelo `Snippet`, vas a poder defender el proyecto con seguridad.

---

## 30. Resumen ultra corto para memorizar

Si necesitas una version muy breve para recordar:

"Es una app Django de CRUD para snippets. La app principal es `vault`. El modelo `Snippet` se guarda en SQLite usando el ORM. Las vistas en `views.py` manejan listar, filtrar, crear, editar y eliminar. Los templates renderizan HTML del lado del servidor. `app.js` solo agrega el copiado al portapapeles. La base se crea con migraciones y se puede poblar con `seed_snippets`."
