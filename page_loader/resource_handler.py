import requests
import logging
import os
from page_loader import url_parser
from .errors import FileError, NetworkError
from pathlib import Path
from progress.bar import PixelBar  # type: ignore
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup  # type: ignore
from requests.exceptions import RequestException


logger = logging.getLogger(__name__)
CHUNK_SIZE = 8192


def get_http(url: str) -> object:
    try:
        response = requests.get(url)  # create HTTP response object
        logger.info('Http response code %s', response.status_code)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()

    except RequestException as req_err:
        logger.error('Network error occurred: %s', req_err)
        raise NetworkError from req_err
    return response.content


def create_res_dir(url: str, output_dir: str):
    dir_name = url_parser.format_dir_url(url)
    dir_full_path = os.path.join(output_dir, dir_name)
    try:
        Path(dir_full_path).mkdir(parents=False, exist_ok=True)
        logger.info('Successfully created directory %s', dir_full_path)
    except OSError as os_err:
        logger.error('Failed to write data into %s', dir_full_path)
        raise FileError from os_err
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
        file_size = r.headers.get('Content-length', 1)
        logger.info('File size %s', file_size)
        with open(path, 'wb') as file:
            aligned_url = url_parser.align_url_len(link, max_url)
            with PixelBar(aligned_url, max=int(file_size), suffix='%(percent)d%%') as bar:  # noqa: E501
                for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                    file.write(chunk)
                    bar.next(CHUNK_SIZE)


def save_result_html(soup: BeautifulSoup, complete_path: str):
    try:
        with open(complete_path, "w", encoding='utf-8') as file:
            file.write(str(soup.prettify(formatter='html5')))
            logger.info('Successfully save file %s', complete_path)
    except OSError as os_err:
        logger.error('Failed to write data into %s', complete_path)
        raise FileError from os_err
