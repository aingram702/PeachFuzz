from urllib.parse import urlparse
import re

def is_valid_url(url: str) -> bool:
    """
    Validates if the provided string is a valid URL.
    Checks for scheme (http/https) and netloc.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
    except ValueError:
        return False

def sanitize_input(input_str: str) -> str:
    """
    Basic sanitization to prevent local command injection if we ever use os.system (we shouldn't).
    Mostly for display purposes or logging.
    """
    if not input_str:
        return ""
    return re.sub(r'[;&|`$]', '', input_str)

def get_domain(url: str) -> str:
    """Extracts domain from URL."""
    try:
        return urlparse(url).netloc
    except:
        return ""
