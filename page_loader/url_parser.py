import re
import os
from urllib.parse import urlparse
from .errors import AppInternalError


def format_file_url(url: str) -> str:
    formatted_url, ext = format_url(url)
    if not ext:
        ext = '.html'
    return '{}{}'.format(formatted_url, ext)


def format_dir_url(url: str) -> str:
    formatted_url, _ = format_url(url)
    return '{}{}'.format(formatted_url, '_files')


def format_url(url: str) -> tuple:
    clean_url = url.strip('/')
    domain = urlparse(clean_url).netloc
    path = urlparse(clean_url).path
    req, ext = os.path.splitext(path)
    formatted_url = replace_non_alphanum_chars_to_dash('{}{}'.format(domain, req))
    return formatted_url, ext


def replace_non_alphanum_chars_to_dash(url: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '-', url)


def is_local_domain(base_url: str, resource_url: str) -> bool:
    if not resource_url:
        return False

    main_domain = urlparse(base_url).hostname
    resource_domain = urlparse(resource_url).hostname

    if resource_domain is None or main_domain is None:
        return True

    return resource_domain == main_domain


def max_url_len(tags: list) -> int:
    if tags:
        return len(max(tags, key=len))
    raise AppInternalError("URL list is empty.")


def align_url_len(url: str, max_len: int) -> str:
    return url.ljust(max_len)
