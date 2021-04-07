import re
import os
from urllib.parse import urlparse
from .errors import AppInternalError


def format_url(url: str, out_type: str) -> str:
    domain = urlparse(url).netloc
    path = urlparse(url).path
    req, ext = os.path.splitext(path)
    formatted_url = replace_to_dash('{}{}'.format(domain, req))

    if out_type == 'file':
        if not ext:
            ext = '.html'
        return '{}{}'.format(formatted_url, ext)
    elif out_type == 'dir':
        return '{}{}'.format(formatted_url, '_files')
    else:
        return 'Wrong type - {}'.format(out_type)


def replace_to_dash(url: str) -> str:
    pattern = re.compile('[^a-zA-Z0-9]')
    return re.sub(pattern, '-', url)


def check_domain(base_url: str, resource_url: str) -> bool:
    if not resource_url:
        return False

    main_domain = urlparse(base_url).hostname
    resource_domain = urlparse(resource_url).hostname

    if resource_domain is None or main_domain is None:
        return True
    elif resource_domain.endswith(main_domain):
        return True
    else:
        return False


def max_url_len(tags: list) -> int:
    if tags:
        return len(max(tags, key=len))
    raise AppInternalError("URL list is empty.")


def align_url_len(url: str, max_len: int) -> str:
    return '{}{}'.format(url, (max_len - len(url)) * ' ')
