import logging
import os
from bs4 import BeautifulSoup  # type: ignore
from page_loader import url_parser  # type: ignore
from urllib.parse import urljoin


logger = logging.getLogger(__name__)


def parse_resource_tags(content: object) -> tuple:
    soup = BeautifulSoup(content, 'html.parser')
    logger.debug('Parsed html body %s', soup)
    all_tags = soup.findAll(['img', 'link', 'script'])
    logger.debug('All tags %s', all_tags)
    return soup, all_tags


def get_local_resource_tags(tags: list, url: str) -> list:
    local_tags = []
    for tag in tags:
        location = get_tag_location(tag.name)
        if not url_parser.check_domain(url, tag.get(location)):
            continue
        local_tags.append(tag)
    return local_tags


def get_urls_list(tags: list, url: str) -> list:
    res_list = []
    for tag in tags:
        location = get_tag_location(tag.name)
        link = urljoin(url, tag.get(location))
        res_list.append(link)
    return res_list


def change_in_soup(tags: list, url: str):
    dir_name = url_parser.format_dir_url(url)
    for tag in tags:
        location = get_tag_location(tag.name)
        link = urljoin(url, tag.get(location))
        res_name = url_parser.format_file_url(link)
        res_file_path = os.path.join(dir_name, res_name)
        tag[location] = res_file_path


def get_tag_location(tag_name: str) -> str:
    return 'href' if tag_name == 'link' else 'src'
