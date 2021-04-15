import requests
import os
import logging
from requests.exceptions import RequestException
from bs4 import BeautifulSoup  # type: ignore
from page_loader import url_parser  # type: ignore
from urllib.parse import urljoin
from .errors import AppInternalError
from progress.bar import PixelBar  # type: ignore
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


logger = logging.getLogger(__name__)


def download(url: str, output_dir: str) -> str:
    content = get_http(url)
    logger.debug('Full http response body %s', content)

    resulting_file_name = url_parser.format_file_url(url)
    complete_path = os.path.join(output_dir, resulting_file_name)

    soup, all_tags = parse_tags(content)

    all_urls = add_to_res_list(all_tags, url)
    change_in_soup(all_tags, url)
    if all_urls:
        dir_full_path = create_res_dir(url, output_dir)
        run_download_res(dir_full_path, all_urls)
    save_result_html(soup, complete_path)
    return complete_path


def get_http(url: str) -> object:
    try:
        response = requests.get(url)  # create HTTP response object
        logger.info('Http response code %s', response.status_code)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()

    except RequestException as req_err:
        logger.error('Network error occurred: %s', req_err)
        raise AppInternalError from req_err
    return response.content


def parse_tags(content: object) -> tuple:
    soup = BeautifulSoup(content, 'html.parser')
    logger.debug('Parsed html body %s', soup)
    all_tags = soup.findAll(['img', 'link', 'script'])
    logger.debug('All tags %s', all_tags)
    return soup, all_tags


def add_to_res_list(tags: list, url: str) -> list:
    res_list = []
    for tag in tags:
        location = get_tag_location(tag.name)
        if not url_parser.check_domain(url, tag.get(location)):
            continue
        link = urljoin(url, tag.get(location))
        res_list.append(link)
    return res_list


def change_in_soup(tags: list, url: str):
    dir_name = url_parser.format_dir_url(url)
    for tag in tags:
        location = get_tag_location(tag.name)
        if not url_parser.check_domain(url, tag.get(location)):
            continue
        link = urljoin(url, tag.get(location))
        res_name = url_parser.format_file_url(link)
        res_file_path = os.path.join(dir_name, res_name)
        tag[location] = res_file_path


def get_tag_location(tag_name: str) -> str:
    return 'href' if tag_name == 'link' else 'src'


def create_res_dir(url: str, output_dir: str):
    dir_name = url_parser.format_dir_url(url)
    dir_full_path = os.path.join(output_dir, dir_name)
    try:
        Path(dir_full_path).mkdir(parents=True, exist_ok=True)
        logger.info('Successfully created directory %s', dir_full_path)
    except OSError as os_err:
        logger.error('Failed to write data into %s', dir_full_path)
        raise AppInternalError from os_err
    return dir_full_path


def run_download_res(dir_full_path: str, all_urls: list):
    max_url = url_parser.max_url_len(all_urls)

    with ThreadPoolExecutor() as executor:
        for link in all_urls:
            res_name = url_parser.format_file_url(link)
            full_file_path = os.path.join(dir_full_path, res_name)
            executor.submit(save_resource, link=link, max_url=max_url, path=full_file_path)  # noqa: E501


def save_resource(link: str, max_url: int, path: str):
    with requests.get(link, stream=True) as r:
        r.raise_for_status()
        logger.info('Saving file %s', path)
        file_size = requests.get(link, stream=True).headers.get('Content-length')  # noqa: E501
        logger.info('File size %s', file_size)
        if file_size is None:
            file_size = '1'
        with open(path, 'wb') as file:
            aligned_url = url_parser.align_url_len(link, max_url)
            with PixelBar(aligned_url, max=int(file_size), suffix='%(percent)d%%') as bar:  # noqa: E501
                for chunk in r.iter_content(chunk_size=8192):
                    file.write(chunk)
                    bar.next(8192)


def save_result_html(soup: BeautifulSoup, complete_path: str):
    try:
        with open(complete_path, "w", encoding='utf-8') as file:
            file.write(str(soup.prettify(formatter='html5')))
            logger.info('Successfully save file %s', complete_path)
    except OSError as os_err:
        logger.error('Failed to write data into %s', complete_path)
        raise AppInternalError from os_err
