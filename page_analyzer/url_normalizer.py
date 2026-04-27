from urllib.parse import urlparse
import validators


def normalize(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}".lower()


def validate(url):
    if not url:
        return False, "URL обязателен"
    
    if len(url) > 255:
        return False, "URL превышает 255 символов"
    
    if not validators.url(url):
        return False, "Некорректный URL"
    
    return True, None