from urllib.parse import urlparse
import validators


def normalize(url):
    parsed = urlparse(url)
    normalized = f"{parsed.scheme}://{parsed.netloc}".lower()
    return normalized.rstrip('/')


def validate(url):

    if not url:
        return False,
    
    if len(url) > 255:
        return False,
    if not validators.url(url):
        return False,
    
    return True, None