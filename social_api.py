import time
import requests

# Caché muy simple en memoria: {account_id: {'data': ..., 'ts': ...}}
# Evita golpear la API de Meta en cada visita a la landing.
_cache = {}
CACHE_TTL_SEGUNDOS = 1800  # 30 minutos

GRAPH_API_VERSION = 'v19.0'
CAMPOS_POST = 'id,caption,media_type,media_url,thumbnail_url,permalink,timestamp'


def obtener_ultimo_post_instagram(access_token, account_id):
    """
    Devuelve un dict con la última publicación de Instagram (o None si falla
    o no hay ninguna), usando la Instagram Graph API. Cachea el resultado
    por cuenta durante CACHE_TTL_SEGUNDOS para no exceder límites de la API
    ni pegarle una request externa a cada visitante de la landing.
    """
    if not access_token or not account_id:
        return None

    ahora = time.time()
    en_cache = _cache.get(account_id)
    if en_cache and (ahora - en_cache['ts']) < CACHE_TTL_SEGUNDOS:
        return en_cache['data']

    url = f'https://graph.facebook.com/{GRAPH_API_VERSION}/{account_id}/media'
    params = {
        'fields': CAMPOS_POST,
        'limit': 1,
        'access_token': access_token,
    }

    post = None
    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json().get('data', [])
        if data:
            post = data[0]
            # Para videos, media_url no siempre es embebible directo; usamos
            # thumbnail_url como imagen de portada si está disponible.
            if post.get('media_type') == 'VIDEO' and post.get('thumbnail_url'):
                post['imagen_mostrar'] = post['thumbnail_url']
            else:
                post['imagen_mostrar'] = post.get('media_url')
    except requests.RequestException:
        # Token vencido, cuenta mal configurada, sin internet, rate limit, etc.
        # Preferimos fallar en silencio y no mostrar el módulo antes que romper la landing.
        post = None

    _cache[account_id] = {'data': post, 'ts': ahora}
    return post


def invalidar_cache(account_id=None):
    """Fuerza a que la próxima consulta ignore la caché (útil tras guardar nuevas credenciales)."""
    if account_id:
        _cache.pop(account_id, None)
    else:
        _cache.clear()