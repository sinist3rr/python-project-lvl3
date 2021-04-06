import requests
import os
import logging
from requests.exceptions import RequestException
from bs4 import BeautifulSoup  # type: ignore
from page_loader import url_parser  # type: ignore
from urllib.parse import urljoin
from .errors import AppInternalError
from progress.bar import PixelBar  # type: ignore


logger = logging.getLogger(__name__)


def download(url: str, output_dir: str) -> str:
    content = get_http(url)
    logger.debug('Full http response body %s', content)

    clean_url = url.strip('/')
    resulting_file_name = url_parser.format_url(clean_url, 'file')
    complete_path = os.path.join(output_dir, resulting_file_name)

    soup, image_tags, link_tags, script_tags = parse_tags(clean_url, content)

    all_urls: list = []
    add_to_res_list(image_tags, url, all_urls)
    add_to_res_list(link_tags, url, all_urls, 'href')
    add_to_res_list(script_tags, url, all_urls)
    logger.debug('All urls %s', all_urls)

    change_in_soup(image_tags, url)
    change_in_soup(link_tags, url, 'href')
    change_in_soup(script_tags, url)

    download_res(url, output_dir, all_urls)
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
        raise AppInternalError('Network error occurred: {}'.format(req_err))
    return response.content


def parse_tags(url: str, content: object) -> tuple:
    soup = BeautifulSoup(content, 'html.parser')
    logger.debug('Parsed html body %s', soup)
    image_tags = soup.findAll('img')
    link_tags = soup.findAll('link')
    script_tags = soup.findAll('script')
    logger.debug('All img tags body %s', image_tags)
    logger.debug('All link tags %s', link_tags)
    logger.debug('All script %s', script_tags)
    return soup, image_tags, link_tags, script_tags


def add_to_res_list(tags: list, url: str, res_list: list, location: str = 'src') -> list:  # noqa: E501
    for tag in tags:
        if not url_parser.check_domain(url, tag.get(location)):
            continue
        link = urljoin(url, tag.get(location))
        res_list.append(link)
    return res_list


def change_in_soup(tags: list, url: str, location: str = 'src'):
    dir_name = url_parser.format_url(url, 'dir')
    for tag in tags:
        if not url_parser.check_domain(url, tag.get(location)):
            continue
        link = urljoin(url, tag.get(location))
        res_name = url_parser.format_url(link, 'file')
        res_file_path = '{}/{}'.format(dir_name, res_name)
        tag[location] = res_file_path


def download_res(url: str, output_dir: str, all_urls: list):
    dir_name = url_parser.format_url(url, 'dir')
    dir_full_path = os.path.join(output_dir, dir_name)
    if not os.path.exists(dir_full_path):
        try:
            os.mkdir(dir_full_path)
            logger.info('Successfully created directory %s', dir_full_path)
        except OSError:
            logger.error('Failed to write data into %s', dir_full_path)
            raise AppInternalError("Directory is not available.")

    for link in all_urls:
        res_name = url_parser.format_url(link, 'file')
        full_file_path = '{}/{}'.format(dir_full_path, res_name)

        with requests.get(link, stream=True) as r:
            r.raise_for_status()
            logger.info('Saving file %s', full_file_path)
            file_size = requests.get(link, stream=True).headers.get('Content-length')  # noqa: E501

            if file_size is None:
                file_size = '1'
            with open(full_file_path, 'wb') as file:
                with PixelBar(link, max=int(file_size), suffix='%(percent)d%%') as bar:  # noqa: E501
                    for chunk in r.iter_content(chunk_size=8192):
                        file.write(chunk)
                        bar.next(8192)


def save_result_html(soup: BeautifulSoup, complete_path: str):
    try:
        with open(complete_path, "w", encoding='utf-8') as file:
            file.write(str(soup.prettify()))
            logger.info('Successfully save file %s', complete_path)
    except OSError:
        logger.error('Failed to write data into %s', complete_path)
        raise AppInternalError("Directory is not available.")
