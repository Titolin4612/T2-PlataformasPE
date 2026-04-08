from django.core.management.base import BaseCommand
from django.db import transaction

from vault.models import Snippet


SAMPLE_SNIPPETS = [
    # ============================================================================
    # GIT - DevOps
    # ============================================================================
    {
        "titulo": "Git: limpiar ramas mergeadas",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Elimina todas las ramas locales que ya han sido mergeadas al main. Útil para mantener el repo limpio.",
        "codigo": """git branch --merged main | grep -v "main" | xargs -r git branch -d""",
        "destacado": True,
    },
    {
        "titulo": "Git: historial compacto por autor",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Muestra un log corto con hash, fecha y autor para revisar actividad reciente.",
        "codigo": """git log --pretty=format:"%C(yellow)%h%Creset %C(cyan)%an%Creset %Cgreen(%cr)%Creset %s" --abbrev-commit -15""",
        "destacado": False,
    },
    {
        "titulo": "Git: revertir último commit sin perder cambios",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Deshace el último commit pero mantiene los cambios en el working directory.",
        "codigo": """git reset --soft HEAD~1""",
        "destacado": True,
    },
    {
        "titulo": "Git: cambiar a rama anterior",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Regresa rápidamente a la rama anterior en la que estabas trabajando.",
        "codigo": """git checkout -""",
        "destacado": False,
    },
    {
        "titulo": "Git: commit amend sin cambiar mensaje",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Añade cambios al último commit sin crear uno nuevo, útil para fixes rápidos.",
        "codigo": """git add .
git commit --amend --no-edit""",
        "destacado": False,
    },
    {
        "titulo": "Git: squash commits en uno",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Combina múltiples commits en uno solo de forma interactiva.",
        "codigo": """git rebase -i HEAD~3""",
        "destacado": False,
    },
    {
        "titulo": "Git: listar commits de hoy",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Muestra todos los commits realizados en las últimas 24 horas.",
        "codigo": """git log --since="24 hours ago" --oneline""",
        "destacado": False,
    },
    {
        "titulo": "Git: ver cambios antes de hacer commit",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Visualiza exactamente qué cambios están en el staging area.",
        "codigo": """git diff --cached""",
        "destacado": False,
    },
    {
        "titulo": "Git: ver contribuidores por commits",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Lista los contribuidores ordenados por cantidad de commits.",
        "codigo": """git shortlog -sn --all""",
        "destacado": True,
    },
    {
        "titulo": "Git: push seguro con force",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Hace push forzado pero de manera segura, verifica que nadie más haya pusheado.",
        "codigo": """git push --force-with-lease""",
        "destacado": False,
    },
    {
        "titulo": "Git: buscar commit que rompió algo",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Usa búsqueda binaria para encontrar el commit que introdujo un bug.",
        "codigo": """git bisect start
git bisect bad HEAD
git bisect good v1.0.0""",
        "destacado": False,
    },
    {
        "titulo": "Git: stash con nombre descriptivo",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Guarda cambios temporalmente con un nombre para recordar qué se guardó.",
        "codigo": """git stash save "descripción del cambio"
git stash list
git stash apply stash@{0}""",
        "destacado": False,
    },
    {
        "titulo": "Git: rebase interactivo en rama remota",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Reescribe el historial de commits de forma interactiva en una rama.",
        "codigo": """git rebase -i origin/main""",
        "destacado": False,
    },
    {
        "titulo": "Git: cherry-pick de un commit específico",
        "lenguaje": "git",
        "categoria": "devops",
        "descripcion": "Aplica un commit específico de otra rama a la rama actual.",
        "codigo": """git cherry-pick <commit-hash>""",
        "destacado": False,
    },

    # ============================================================================
    # GIT - Utilidades
    # ============================================================================
    {
        "titulo": "Git: crear alias global para comando personalizado",
        "lenguaje": "git",
        "categoria": "utils",
        "descripcion": "Define un alias global que ejecuta un script bash personalizado.",
        "codigo": """git config --global alias.clean-all '!git clean -fd && git reset --hard'""",
        "destacado": False,
    },
    {
        "titulo": "Git: ver tamaño de cada rama",
        "lenguaje": "git",
        "categoria": "utils",
        "descripcion": "Muestra cuántos commits diferencia hay entre cada rama y main.",
        "codigo": """git for-each-ref --sort=-committerdate refs/heads/ --format='%(refname:short) %(committerdate:short)'""",
        "destacado": False,
    },
    {
        "titulo": "Git: eliminar tag local y remoto",
        "lenguaje": "git",
        "categoria": "utils",
        "descripcion": "Borra un tag tanto en el repositorio local como en el remoto.",
        "codigo": """git tag -d v1.0.0
git push origin :refs/tags/v1.0.0""",
        "destacado": False,
    },
    {
        "titulo": "Git: configurar nombre y email",
        "lenguaje": "git",
        "categoria": "utils",
        "descripcion": "Establece el usuario global de git para que aparezca en los commits.",
        "codigo": """git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com\"""",
        "destacado": False,
    },
    {
        "titulo": "Git: ignorar cambios en archivo ya trackeado",
        "lenguaje": "git",
        "categoria": "utils",
        "descripcion": "Deja de trackear cambios en un archivo sin eliminarlo del repositorio.",
        "codigo": """git update-index --assume-unchanged config.local.js""",
        "destacado": False,
    },
    {
        "titulo": "Git: volver a trackear archivo ignorado",
        "lenguaje": "git",
        "categoria": "utils",
        "descripcion": "Vuelve a empezar a trackear los cambios en un archivo previamente ignorado.",
        "codigo": """git update-index --no-assume-unchanged config.local.js""",
        "destacado": False,
    },

    # ============================================================================
    # BASH - DevOps
    # ============================================================================
    {
        "titulo": "Bash: matar proceso por puerto",
        "lenguaje": "bash",
        "categoria": "devops",
        "descripcion": "Encuentra y termina el proceso que está usando un puerto específico.",
        "codigo": """PID=$(lsof -ti :8000)
if [ -n "$PID" ]; then
  kill -9 "$PID"
fi""",
        "destacado": True,
    },
    {
        "titulo": "Bash: esperar a que puerto esté disponible",
        "lenguaje": "bash",
        "categoria": "devops",
        "descripcion": "Espera de forma activa a que un puerto esté disponible antes de continuar.",
        "codigo": """while ! nc -z localhost 5432; do
  echo "Esperando base de datos..."
  sleep 1
done
echo "Base de datos lista"
""",
        "destacado": False,
    },
    {
        "titulo": "Bash: crear backup con timestamp",
        "lenguaje": "bash",
        "categoria": "devops",
        "descripcion": "Empaqueta una carpeta en un archivo comprimido con fecha y hora.",
        "codigo": """backup_name="project-$(date +%Y%m%d-%H%M%S).tar.gz"
tar -czf "$backup_name" ./project""",
        "destacado": False,
    },
    {
        "titulo": "Bash: monitorear cambios en archivo",
        "lenguaje": "bash",
        "categoria": "devops",
        "descripcion": "Ejecuta un comando cada vez que detecta cambios en un archivo.",
        "codigo": """while inotifywait -e modify app.js; do
  echo "Archivo modificado"
  npm restart
done""",
        "destacado": False,
    },
    {
        "titulo": "Bash: verificar si comando existe",
        "lenguaje": "bash",
        "categoria": "devops",
        "descripcion": "Comprueba si un comando específico está disponible en el sistema.",
        "codigo": """if command -v docker &> /dev/null; then
  echo "Docker está instalado"
else
  echo "Docker no está instalado"
fi""",
        "destacado": False,
    },
    {
        "titulo": "Bash: ejecutar script si existe",
        "lenguaje": "bash",
        "categoria": "devops",
        "descripcion": "Verifica que un archivo exista y sea ejecutable antes de correrlo.",
        "codigo": """script="./deploy.sh"
if [ -x "$script" ]; then
  "$script"
else
  echo "Script no encontrado o no es ejecutable"
fi""",
        "destacado": False,
    },
    {
        "titulo": "Bash: obtener tamaño de carpeta",
        "lenguaje": "bash",
        "categoria": "devops",
        "descripcion": "Calcula el tamaño total de un directorio en formato legible.",
        "codigo": """du -sh ./project""",
        "destacado": False,
    },
    {
        "titulo": "Bash: buscar y reemplazar en múltiples archivos",
        "lenguaje": "bash",
        "categoria": "devops",
        "descripcion": "Encuentra y reemplaza texto en todos los archivos de un tipo específico.",
        "codigo": """find . -name "*.js" -type f -exec sed -i 's/oldValue/newValue/g' {} +""",
        "destacado": False,
    },
    {
        "titulo": "Bash: ejecutar comando en paralelo",
        "lenguaje": "bash",
        "categoria": "devops",
        "descripcion": "Corre múltiples comandos en paralelo y espera a que todos terminen.",
        "codigo": """npm run build & 
npm run test & 
wait
echo "Todos los procesos completados"
""",
        "destacado": False,
    },
    {
        "titulo": "Bash: retardar ejecución",
        "lenguaje": "bash",
        "categoria": "devops",
        "descripcion": "Pausa la ejecución del script por un tiempo determinado.",
        "codigo": """sleep 5  # Espera 5 segundos
sleep 2m # Espera 2 minutos""",
        "destacado": False,
    },

    # ============================================================================
    # BASH - Utilidades
    # ============================================================================
    {
        "titulo": "Bash: crear carpeta si no existe",
        "lenguaje": "bash",
        "categoria": "utils",
        "descripcion": "Verifica que una carpeta existe, si no la crea.",
        "codigo": """mkdir -p ./data/uploads""",
        "destacado": False,
    },
    {
        "titulo": "Bash: listar archivos ordenados por tamaño",
        "lenguaje": "bash",
        "categoria": "utils",
        "descripcion": "Muestra los archivos de una carpeta ordenados por tamaño en descendente.",
        "codigo": """ls -lhSr""",
        "destacado": False,
    },
    {
        "titulo": "Bash: extraer archivo comprimido",
        "lenguaje": "bash",
        "categoria": "utils",
        "descripcion": "Descomprime un archivo basándose en su extensión automáticamente.",
        "codigo": """file="archive.tar.gz"
tar -xzf "$file\"""",
        "destacado": False,
    },
    {
        "titulo": "Bash: contar líneas de código",
        "lenguaje": "bash",
        "categoria": "utils",
        "descripcion": "Cuenta todas las líneas de código en archivos de un tipo específico.",
        "codigo": """find . -name "*.js" -type f | xargs wc -l | tail -1""",
        "destacado": False,
    },
    {
        "titulo": "Bash: obtener timestamp actual",
        "lenguaje": "bash",
        "categoria": "utils",
        "descripcion": "Obtiene la fecha y hora actual en diferentes formatos.",
        "codigo": """date +%s                    # Unix timestamp
date +%Y-%m-%d             # YYYY-MM-DD
date +%Y%m%d_%H%M%S       # YYYYMMDD_HHMMSS""",
        "destacado": False,
    },
    {
        "titulo": "Bash: leer variable de archivo .env",
        "lenguaje": "bash",
        "categoria": "utils",
        "descripcion": "Carga variables de entorno desde un archivo .env sin usar paquetes externos.",
        "codigo": """export $(grep -v '^#' .env | xargs)
echo $DATABASE_URL""",
        "destacado": False,
    },

    # ============================================================================
    # PYTHON - Backend
    # ============================================================================
    {
        "titulo": "Python: slug simple sin dependencias",
        "lenguaje": "python",
        "categoria": "backend",
        "descripcion": "Convierte un título en un slug limpio usando solo la librería estándar.",
        "codigo": """import re
import unicodedata


def simple_slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")""",
        "destacado": True,
    },
    {
        "titulo": "Python: reintento HTTP con backoff exponencial",
        "lenguaje": "python",
        "categoria": "backend",
        "descripcion": "Realiza reintentos automáticos con espera exponencial para llamadas HTTP.",
        "codigo": """import time
import requests


def get_with_retry(url: str, retries: int = 3, timeout: int = 5):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)""",
        "destacado": True,
    },
    {
        "titulo": "Python: decorador para medir tiempo de ejecución",
        "lenguaje": "python",
        "categoria": "backend",
        "descripcion": "Envuelve cualquier función para medir y registrar su tiempo de ejecución.",
        "codigo": """import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} tardó {elapsed:.2f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(2)""",
        "destacado": True,
    },
    {
        "titulo": "Python: decorador para reintentos automáticos",
        "lenguaje": "python",
        "categoria": "backend",
        "descripcion": "Retry automático con backoff para cualquier función que lance excepciones.",
        "codigo": """import time
from functools import wraps


def retry(max_attempts: int = 3, wait_seconds: int = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(wait_seconds ** attempt)
        return wrapper
    return decorator

@retry(max_attempts=3)
def unstable_function():
    pass""",
        "destacado": True,
    },
    {
        "titulo": "Python: parsear argumentos de línea de comandos",
        "lenguaje": "python",
        "categoria": "backend",
        "descripcion": "Lee y procesa argumentos pasados a un script desde la terminal.",
        "codigo": """import argparse


parser = argparse.ArgumentParser(description="Mi script")
parser.add_argument("--host", default="localhost", help="Host")
parser.add_argument("--port", type=int, default=8000, help="Puerto")
parser.add_argument("--debug", action="store_true", help="Modo debug")

args = parser.parse_args()
print(f"Host: {args.host}, Puerto: {args.port}, Debug: {args.debug}")""",
        "destacado": False,
    },
    {
        "titulo": "Python: leer archivo de configuración JSON",
        "lenguaje": "python",
        "categoria": "backend",
        "descripcion": "Carga y parsea un archivo JSON de configuración de forma segura.",
        "codigo": """import json
from pathlib import Path


def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as f:
        return json.load(f)

config = load_config("config.json")
print(config["database"]["host"])""",
        "destacado": False,
    },
    {
        "titulo": "Python: crear hash seguro de contraseña",
        "lenguaje": "python",
        "categoria": "backend",
        "descripcion": "Genera y verifica hashes seguros de contraseñas usando bcrypt.",
        "codigo": """import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

hashed = hash_password("mi_contraseña")
print(verify_password("mi_contraseña", hashed))""",
        "destacado": False,
    },
    {
        "titulo": "Python: procesar archivo CSV grande",
        "lenguaje": "python",
        "categoria": "backend",
        "descripcion": "Lee un CSV grande en chunks para no sobrecargar la memoria.",
        "codigo": """import pandas as pd


chunk_size = 10000
for chunk in pd.read_csv("datos_grandes.csv", chunksize=chunk_size):
    # Procesar cada chunk
    print(f"Procesando {len(chunk)} filas")
    # hacer algo con chunk""",
        "destacado": False,
    },
    {
        "titulo": "Python: ejecutar función en background con threading",
        "lenguaje": "python",
        "categoria": "backend",
        "descripcion": "Ejecuta una función en un thread separado sin bloquear el programa.",
        "codigo": """import threading
import time


def background_task():
    for i in range(5):
        print(f"Tarea background: {i}")
        time.sleep(1)

thread = threading.Thread(target=background_task, daemon=True)
thread.start()
print("Continuando con el programa principal")""",
        "destacado": False,
    },
    {
        "titulo": "Python: medir uso de memoria de función",
        "lenguaje": "python",
        "categoria": "backend",
        "descripcion": "Monitorea cuánta memoria usa una función durante su ejecución.",
        "codigo": """import tracemalloc


tracemalloc.start()

lista_grande = [i for i in range(1000000)]

current, peak = tracemalloc.get_traced_memory()
print(f"Memoria actual: {current / 1024 / 1024:.2f} MB")
print(f"Memoria pico: {peak / 1024 / 1024:.2f} MB")
tracemalloc.stop()""",
        "destacado": False,
    },
    {
        "titulo": "Python: validador de email simple",
        "lenguaje": "python",
        "categoria": "backend",
        "descripcion": "Valida si un string es un email con formato correcto.",
        "codigo": """import re


def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

print(is_valid_email("usuario@ejemplo.com"))""",
        "destacado": False,
    },

    # ============================================================================
    # PYTHON - Utilidades
    # ============================================================================
    {
        "titulo": "Python: crear archivo temporal",
        "lenguaje": "python",
        "categoria": "utils",
        "descripcion": "Crea un archivo temporal que se elimina automáticamente al terminar.",
        "codigo": """import tempfile


with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
    tmp.write("datos temporales")
    print(f"Archivo: {tmp.name}")

# Se elimina automáticamente al salir del context manager""",
        "destacado": False,
    },
    {
        "titulo": "Python: medir distancia entre dos strings (Levenshtein)",
        "lenguaje": "python",
        "categoria": "utils",
        "descripcion": "Calcula la similitud entre dos strings contando diferencias mínimas.",
        "codigo": """from difflib import SequenceMatcher


def string_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

print(string_similarity("hello", "hallo"))  # 0.8""",
        "destacado": False,
    },
    {
        "titulo": "Python: generar colores aleatorios",
        "lenguaje": "python",
        "categoria": "utils",
        "descripcion": "Genera códigos hexadecimales de colores aleatorios.",
        "codigo": """import random


def random_color() -> str:
    return f"#{random.randint(0, 0xFFFFFF):06x}"

print(random_color())  # #a3c2f1""",
        "destacado": False,
    },
    {
        "titulo": "Python: listado comprensivo con condición",
        "lenguaje": "python",
        "categoria": "utils",
        "descripcion": "Crea listas de forma compacta usando comprensiones con filtros.",
        "codigo": """# Obtener números pares del 0 al 10
pares = [x for x in range(11) if x % 2 == 0]

# Transformar y filtrar
numeros = [1, 2, 3, 4, 5]
resultado = [x * 2 for x in numeros if x > 2]
print(resultado)  # [6, 8, 10]""",
        "destacado": False,
    },
    {
        "titulo": "Python: aplanar lista de listas",
        "lenguaje": "python",
        "categoria": "utils",
        "descripcion": "Convierte una lista de listas en una sola lista.",
        "codigo": """matriz = [[1, 2], [3, 4], [5, 6]]

# Opción 1: Comprensión
aplanado = [x for fila in matriz for x in fila]

# Opción 2: itertools
import itertools
aplanado = list(itertools.chain.from_iterable(matriz))

print(aplanado)  # [1, 2, 3, 4, 5, 6]""",
        "destacado": False,
    },

    # ============================================================================
    # JAVASCRIPT - Frontend
    # ============================================================================
    {
        "titulo": "JavaScript: debounce para búsqueda",
        "lenguaje": "javascript",
        "categoria": "frontend",
        "descripcion": "Retrasa la ejecución de una función para evitar disparar múltiples peticiones.",
        "codigo": """function debounce(fn, wait = 250) {
  let timeoutId;

  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), wait);
  };
}

const handleSearch = debounce((query) => {
  console.log("Buscando:", query);
}, 300);""",
        "destacado": True,
    },
    {
        "titulo": "JavaScript: copiar texto con fallback",
        "lenguaje": "javascript",
        "categoria": "frontend",
        "descripcion": "Copia texto al portapapeles con soporte para navegadores antiguos.",
        "codigo": """async function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const helper = document.createElement("textarea");
  helper.value = text;
  document.body.appendChild(helper);
  helper.select();
  document.execCommand("copy");
  document.body.removeChild(helper);
}""",
        "destacado": True,
    },
    {
        "titulo": "JavaScript: throttle para eventos frecuentes",
        "lenguaje": "javascript",
        "categoria": "frontend",
        "descripcion": "Limita la frecuencia de ejecución de una función a un intervalo mínimo.",
        "codigo": """function throttle(fn, limit = 250) {
  let inThrottle;
  
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

window.addEventListener('resize', throttle(() => {
  console.log('Window resized');
}, 500));""",
        "destacado": True,
    },
    {
        "titulo": "JavaScript: detectar si dispositivo es móvil",
        "lenguaje": "javascript",
        "categoria": "frontend",
        "descripcion": "Verifica si el usuario está en un dispositivo móvil o de escritorio.",
        "codigo": """function isMobile() {
  const userAgent = navigator.userAgent;
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent);
}

if (isMobile()) {
  console.log("Usuario en móvil");
}""",
        "destacado": False,
    },
    {
        "titulo": "JavaScript: hacer petición HTTP con retry",
        "lenguaje": "javascript",
        "categoria": "frontend",
        "descripcion": "Realiza una petición fetch con reintentos automáticos.",
        "codigo": """async function fetchWithRetry(url, options = {}, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, options);
      if (response.ok) return response.json();
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(r => setTimeout(r, 2 ** i * 1000));
    }
  }
}""",
        "destacado": False,
    },
    {
        "titulo": "JavaScript: format de número con separadores",
        "lenguaje": "javascript",
        "categoria": "frontend",
        "descripcion": "Formatea un número para mostrar con miles separados.",
        "codigo": """function formatNumber(num) {
  return new Intl.NumberFormat('es-CO').format(num);
}

console.log(formatNumber(1234567));  // 1.234.567""",
        "destacado": False,
    },
    {
        "titulo": "JavaScript: validador de email",
        "lenguaje": "javascript",
        "categoria": "frontend",
        "descripcion": "Valida si un string tiene formato de email válido.",
        "codigo": """function isValidEmail(email) {
  const regex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
  return regex.test(email);
}

console.log(isValidEmail("usuario@ejemplo.com"));""",
        "destacado": False,
    },
    {
        "titulo": "JavaScript: generar ID único",
        "lenguaje": "javascript",
        "categoria": "frontend",
        "descripcion": "Genera un identificador único para elementos o transacciones.",
        "codigo": """function generateId() {
  return Math.random().toString(36).substring(2) + Date.now().toString(36);
}

console.log(generateId());  // "8xk3j2x01234567890abc\"""",
        "destacado": False,
    },
    {
        "titulo": "JavaScript: obtener parámetros de URL",
        "lenguaje": "javascript",
        "categoria": "frontend",
        "descripcion": "Extrae y parsea los parámetros de la query string de una URL.",
        "codigo": """function getURLParams() {
  const params = new URLSearchParams(window.location.search);
  return Object.fromEntries(params);
}

// En URL: ?id=123&name=John
console.log(getURLParams());  // { id: '123', name: 'John' }""",
        "destacado": False,
    },
    {
        "titulo": "JavaScript: dark mode toggle",
        "lenguaje": "javascript",
        "categoria": "frontend",
        "descripcion": "Alterna entre tema claro y oscuro con persistencia en localStorage.",
        "codigo": """function toggleDarkMode() {
  const html = document.documentElement;
  const isDark = html.getAttribute('data-theme') === 'dark';
  
  html.setAttribute('data-theme', isDark ? 'light' : 'dark');
  localStorage.setItem('theme', isDark ? 'light' : 'dark');
}

// Cargar tema guardado
const saved = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', saved);""",
        "destacado": False,
    },
    {
        "titulo": "JavaScript: lazy load de imágenes",
        "lenguaje": "javascript",
        "categoria": "frontend",
        "descripcion": "Carga imágenes solo cuando aparecen en el viewport.",
        "codigo": """const images = document.querySelectorAll('img[data-src]');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      observer.unobserve(img);
    }
  });
});

images.forEach(img => observer.observe(img));""",
        "destacado": False,
    },

    # ============================================================================
    # SQL - Database
    # ============================================================================
    {
        "titulo": "SQL: top consultas por duración",
        "lenguaje": "sql",
        "categoria": "database",
        "descripcion": "Encuentra las consultas más lentas en la base de datos.",
        "codigo": """SELECT query_text,
       COUNT(*) AS total_runs,
       ROUND(AVG(duration_ms), 2) AS avg_duration_ms
FROM query_logs
WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY query_text
ORDER BY avg_duration_ms DESC
LIMIT 10;""",
        "destacado": True,
    },
    {
        "titulo": "SQL: paginación con ROW_NUMBER",
        "lenguaje": "sql",
        "categoria": "database",
        "descripcion": "Implementa paginación usando funciones de ventana.",
        "codigo": """WITH ranked_users AS (
  SELECT id,
         email,
         ROW_NUMBER() OVER (ORDER BY created_at DESC) AS row_num
  FROM users
)
SELECT id, email
FROM ranked_users
WHERE row_num BETWEEN 21 AND 40;""",
        "destacado": True,
    },
    {
        "titulo": "SQL: encontrar duplicados",
        "lenguaje": "sql",
        "categoria": "database",
        "descripcion": "Identifica registros duplicados en una tabla.",
        "codigo": """SELECT email,
       COUNT(*) as count
FROM users
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY count DESC;""",
        "destacado": False,
    },
    {
        "titulo": "SQL: eliminar duplicados manteniendo el primero",
        "lenguaje": "sql",
        "categoria": "database",
        "descripcion": "Elimina registros duplicados pero mantiene la primera instancia.",
        "codigo": """DELETE FROM users
WHERE id NOT IN (
  SELECT MIN(id)
  FROM users
  GROUP BY email
);""",
        "destacado": False,
    },
    {
        "titulo": "SQL: actualizar con datos de otra tabla",
        "lenguaje": "sql",
        "categoria": "database",
        "descripcion": "Actualiza una tabla basándose en datos de otra tabla.",
        "codigo": """UPDATE users
SET department = (
  SELECT department FROM employees 
  WHERE employees.user_id = users.id
)
WHERE id IN (
  SELECT user_id FROM employees
);""",
        "destacado": False,
    },
    {
        "titulo": "SQL: obtener N registros aleatorios",
        "lenguaje": "sql",
        "categoria": "database",
        "descripcion": "Selecciona registros al azar de una tabla.",
        "codigo": """SELECT * FROM products
ORDER BY RANDOM()
LIMIT 10;""",
        "destacado": False,
    },
    {
        "titulo": "SQL: ranking con RANK vs ROW_NUMBER",
        "lenguaje": "sql",
        "categoria": "database",
        "descripcion": "Muestra la diferencia entre RANK y ROW_NUMBER en ventanas.",
        "codigo": """SELECT name,
       salary,
       RANK() OVER (ORDER BY salary DESC) as rank,
       ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num
FROM employees;""",
        "destacado": False,
    },
    {
        "titulo": "SQL: ejecutar mismo query por cada fila",
        "lenguaje": "sql",
        "categoria": "database",
        "descripcion": "Genera múltiples queries dinámica para cada registro.",
        "codigo": """SELECT 'UPDATE users SET active = false WHERE id = ' || id || ';'
FROM users
WHERE last_login < CURRENT_DATE - INTERVAL '30 days';""",
        "destacado": False,
    },
    {
        "titulo": "SQL: calcular cumulative sum",
        "lenguaje": "sql",
        "categoria": "database",
        "descripcion": "Calcula suma acumulada usando window functions.",
        "codigo": """SELECT date,
       amount,
       SUM(amount) OVER (ORDER BY date) as cumulative_total
FROM transactions
ORDER BY date;""",
        "destacado": False,
    },
    {
        "titulo": "SQL: encontrar brechas en secuencias",
        "lenguaje": "sql",
        "categoria": "database",
        "descripcion": "Identifica números faltantes en una secuencia.",
        "codigo": """WITH numbered AS (
  SELECT id,
         ROW_NUMBER() OVER (ORDER BY id) as row_num
  FROM products
)
SELECT id FROM numbered
WHERE id != row_num;""",
        "destacado": False,
    },

    # ============================================================================
    # DJANGO - Backend
    # ============================================================================
    {
        "titulo": "Django: queryset optimizado para detalle",
        "lenguaje": "django",
        "categoria": "backend",
        "descripcion": "Reduce consultas N+1 usando select_related y prefetch_related.",
        "codigo": """from blog.models import Post

post = (
    Post.objects.select_related("author")
    .prefetch_related("tags", "comments__user")
    .get(pk=post_id)
)""",
        "destacado": True,
    },
    {
        "titulo": "Django: crear superusuario en seed",
        "lenguaje": "django",
        "categoria": "backend",
        "descripcion": "Automatiza la creación del admin sin duplicar registros.",
        "codigo": """from django.contrib.auth import get_user_model

User = get_user_model()
User.objects.get_or_create(
    username="admin",
    defaults={
        "email": "admin@example.com",
        "is_staff": True,
        "is_superuser": True,
        "password": "admin123",
    },
)""",
        "destacado": False,
    },
    {
        "titulo": "Django: custom manager para queryset reutilizable",
        "lenguaje": "django",
        "categoria": "backend",
        "descripcion": "Define un manager personalizado para queries frecuentes.",
        "codigo": """from django.db import models

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Article(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    
    objects = models.Manager()
    published = PublishedManager()

# Uso
Article.published.all()""",
        "destacado": False,
    },
    {
        "titulo": "Django: signals para acciones automáticas",
        "lenguaje": "django",
        "categoria": "backend",
        "descripcion": "Ejecuta código automáticamente cuando se crea o actualiza un modelo.",
        "codigo": """from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(f"Nuevo usuario: {instance.username}")

# O regístrate explícitamente
post_save.connect(create_user_profile, sender=User)""",
        "destacado": False,
    },
    {
        "titulo": "Django: paginación con cursor",
        "lenguaje": "django",
        "categoria": "backend",
        "descripcion": "Pagina resultados eficientemente usando cursors en lugar de offset.",
        "codigo": """from rest_framework.pagination import CursorPagination

class PostPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at'
    cursor_query_param = 'cursor'

class PostViewSet(viewsets.ModelViewSet):
    pagination_class = PostPagination""",
        "destacado": False,
    },
    {
        "titulo": "Django: validador personalizado para modelos",
        "lenguaje": "django",
        "categoria": "backend",
        "descripcion": "Crea validaciones personalizadas para campos de modelo.",
        "codigo": """from django.core.exceptions import ValidationError
from django.db import models

def validate_even_number(value):
    if value % 2 != 0:
        raise ValidationError("El número debe ser par.")

class MyModel(models.Model):
    number = models.IntegerField(validators=[validate_even_number])""",
        "destacado": False,
    },
    {
        "titulo": "Django: queryset anotado con agregaciones",
        "lenguaje": "django",
        "categoria": "backend",
        "descripcion": "Añade campos calculados a un queryset usando agregaciones.",
        "codigo": """from django.db.models import Count, Avg
from blog.models import Author

authors = (
    Author.objects
    .annotate(total_posts=Count('posts'))
    .annotate(avg_rating=Avg('posts__rating'))
    .filter(total_posts__gte=5)
)""",
        "destacado": False,
    },
    {
        "titulo": "Django: bulk create para inserciones masivas",
        "lenguaje": "django",
        "categoria": "backend",
        "descripcion": "Inserta múltiples registros de una sola vez para mayor eficiencia.",
        "codigo": """from blog.models import Post

posts = [
    Post(title="Post 1", content="..."),
    Post(title="Post 2", content="..."),
    Post(title="Post 3", content="..."),
]
Post.objects.bulk_create(posts, batch_size=500)""",
        "destacado": False,
    },
    {
        "titulo": "Django: filtrar por fecha reciente",
        "lenguaje": "django",
        "categoria": "backend",
        "descripcion": "Filtra registros creados en un rango de tiempo específico.",
        "codigo": """from django.utils import timezone
from datetime import timedelta
from blog.models import Post

week_ago = timezone.now() - timedelta(days=7)
recent_posts = Post.objects.filter(created_at__gte=week_ago)""",
        "destacado": False,
    },
    {
        "titulo": "Django: exclude para filtrado negativo",
        "lenguaje": "django",
        "categoria": "backend",
        "descripcion": "Filtra excluyendo registros que cumplan una condición.",
        "codigo": """from blog.models import Post

# Obtener todos excepto los borradores
published = Post.objects.exclude(status='draft')

# Usar Q para lógica compleja
from django.db.models import Q
filtered = Post.objects.exclude(
    Q(status='draft') | Q(author__is_active=False)
)""",
        "destacado": False,
    },

    # ============================================================================
    # HTML - Frontend
    # ============================================================================
    {
        "titulo": "HTML: estructura básica de página moderna",
        "lenguaje": "html",
        "categoria": "frontend",
        "descripcion": "Template HTML5 con metaetiquetas esenciales y atributos modernos.",
        "codigo": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Descripción de la página">
    <title>Mi Sitio</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <nav>Navegación</nav>
    </header>
    <main>
        <section>Contenido</section>
    </main>
    <footer>Pie de página</footer>
    <script src="script.js"></script>
</body>
</html>""",
        "destacado": False,
    },
    {
        "titulo": "HTML: form con validación integrada",
        "lenguaje": "html",
        "categoria": "frontend",
        "descripcion": "Formulario HTML5 con validación nativa del navegador.",
        "codigo": """<form method="POST" action="/submit">
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required>
    
    <label for="password">Contraseña:</label>
    <input type="password" id="password" name="password" minlength="8" required>
    
    <label for="age">Edad:</label>
    <input type="number" id="age" name="age" min="18" max="120">
    
    <button type="submit">Enviar</button>
    <button type="reset">Limpiar</button>
</form>""",
        "destacado": False,
    },
    {
        "titulo": "HTML: semantic HTML para accesibilidad",
        "lenguaje": "html",
        "categoria": "frontend",
        "descripcion": "Estructura semántica que mejora accesibilidad y SEO.",
        "codigo": """<article>
    <header>
        <h1>Título del artículo</h1>
        <time datetime="2024-01-15">15 de enero, 2024</time>
    </header>
    
    <section>
        <p>Contenido principal...</p>
    </section>
    
    <aside>
        <h3>Información relacionada</h3>
    </aside>
</article>""",
        "destacado": False,
    },
    {
        "titulo": "HTML: meta tags para redes sociales",
        "lenguaje": "html",
        "categoria": "frontend",
        "descripcion": "Open Graph y Twitter Card para compartir en redes sociales.",
        "codigo": """<meta property="og:title" content="Mi Sitio">
<meta property="og:description" content="Descripción">
<meta property="og:image" content="imagen.jpg">
<meta property="og:url" content="https://ejemplo.com">
<meta property="og:type" content="website">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Mi Sitio">
<meta name="twitter:description" content="Descripción">
<meta name="twitter:image" content="imagen.jpg">""",
        "destacado": False,
    },

    # ============================================================================
    # CSS - Frontend
    # ============================================================================
    {
        "titulo": "CSS: flexbox para centrado perfecto",
        "lenguaje": "css",
        "categoria": "frontend",
        "descripcion": "Centra contenido horizontal y verticalmente con flexbox.",
        "codigo": """.container {
    display: flex;
    justify-content: center;  /* Centro horizontal */
    align-items: center;      /* Centro vertical */
    height: 100vh;            /* Altura de viewport */
}""",
        "destacado": True,
    },
    {
        "titulo": "CSS: grid responsiva sin media queries",
        "lenguaje": "css",
        "categoria": "frontend",
        "descripcion": "Grid que se adapta automáticamente sin breakpoints.",
        "codigo": """.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
}

/* Cada item toma mínimo 250px, máximo 1fr */""",
        "destacado": False,
    },
    {
        "titulo": "CSS: dark mode con variables",
        "lenguaje": "css",
        "categoria": "frontend",
        "descripcion": "Sistema de temas usando CSS custom properties.",
        "codigo": """:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f5f5f5;
    --text-primary: #000000;
    --text-secondary: #666666;
}

:root[data-theme="dark"] {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2d2d2d;
    --text-primary: #ffffff;
    --text-secondary: #999999;
}

body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
}""",
        "destacado": False,
    },
    {
        "titulo": "CSS: animación suave de scroll",
        "lenguaje": "css",
        "categoria": "frontend",
        "descripcion": "Scroll suave y animaciones elegantes al cargar.",
        "codigo": """html {
    scroll-behavior: smooth;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.card {
    animation: fadeIn 0.5s ease-out;
}""",
        "destacado": False,
    },
    {
        "titulo": "CSS: truncar texto con ellipsis",
        "lenguaje": "css",
        "categoria": "frontend",
        "descripcion": "Corta texto largo y agrega puntos suspensivos.",
        "codigo": """/* Una línea */
.truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Múltiples líneas */
.truncate-lines {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}""",
        "destacado": False,
    },
    {
        "titulo": "CSS: responsive images",
        "lenguaje": "css",
        "categoria": "frontend",
        "descripcion": "Imágenes que se adaptan al tamaño del contenedor.",
        "codigo": """img {
    max-width: 100%;
    height: auto;
    display: block;
}

/* Mantener aspect ratio */
.image-container {
    aspect-ratio: 16 / 9;
    overflow: hidden;
}""",
        "destacado": False,
    },

    # ============================================================================
    # Otros lenguajes - Backend
    # ============================================================================
    {
        "titulo": "Docker: Dockerfile básico para Python",
        "lenguaje": "docker",
        "categoria": "devops",
        "descripcion": "Configuración Docker mínima para aplicación Python.",
        "codigo": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]""",
        "destacado": False,
    },
    {
        "titulo": "Docker: docker-compose para stack completo",
        "lenguaje": "docker",
        "categoria": "devops",
        "descripcion": "Compone múltiples servicios (app, db, redis) en un archivo.",
        "codigo": """version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:""",
        "destacado": False,
    },
    {
        "titulo": "Regex: validar URL",
        "lenguaje": "regex",
        "categoria": "utils",
        "descripcion": "Expresión regular para validar URLs.",
        "codigo": """^(https?:\\/\\/)?(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b([-a-zA-Z0-9()@:%_\\+.~#?&//=]*)$""",
        "destacado": False,
    },
    {
        "titulo": "Regex: extraer números de texto",
        "lenguaje": "regex",
        "categoria": "utils",
        "descripcion": "Patrón para encontrar todos los números en un texto.",
        "codigo": """\\d+(?:\\.\\d+)?""",
        "destacado": False,
    },
    {
        "titulo": "Regex: validar contraseña fuerte",
        "lenguaje": "regex",
        "categoria": "utils",
        "descripcion": "Validar que contraseña tenga mayúsculas, números y caracteres especiales.",
        "codigo": """^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$""",
        "destacado": False,
    },
    {
        "titulo": "JSON: estructura de API response",
        "lenguaje": "json",
        "categoria": "backend",
        "descripcion": "Formato estándar para respuestas de API RESTful.",
        "codigo": """{
  "success": true,
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "1.0"
  },
  "errors": null
}""",
        "destacado": False,
    },
    {
        "titulo": "YAML: configuración de aplicación",
        "lenguaje": "yaml",
        "categoria": "devops",
        "descripcion": "Archivo de configuración YAML para aplicaciones.",
        "codigo": """application:
  name: Mi App
  version: 1.0.0
  debug: false

database:
  host: localhost
  port: 5432
  name: myapp_db
  credentials:
    user: postgres
    password: ${DB_PASSWORD}

logging:
  level: INFO
  format: json
  handlers:
    - file: logs/app.log
    - console""",
        "destacado": False,
    },
]


class Command(BaseCommand):
    help = "Carga snippets completos para desarrollo sin duplicarlos."

    @transaction.atomic
    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for item in SAMPLE_SNIPPETS:
            _, created = Snippet.objects.update_or_create(
                titulo=item["titulo"],
                defaults={
                    "lenguaje": item["lenguaje"],
                    "categoria": item["categoria"],
                    "descripcion": item["descripcion"],
                    "codigo": item["codigo"],
                    "destacado": item["destacado"],
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        total_count = Snippet.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Seed completado: {created_count} creados, {updated_count} actualizados, {total_count} snippets disponibles."
            )
        )
