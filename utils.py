import re
import unicodedata


def generar_slug(texto):
    """Convierte un título en un slug URL-friendly (ej: 'Mi Post!' -> 'mi-post')."""
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')
    texto = re.sub(r'[^\w\s-]', '', texto).strip().lower()
    return re.sub(r'[\s_-]+', '-', texto)