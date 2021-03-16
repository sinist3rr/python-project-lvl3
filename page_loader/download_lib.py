import requests
import os
import logging
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup  # type: ignore
from page_loader import url_parser  # type: ignore
from urllib.parse import urljoin


logger = logging.getLogger(__name__)


def download(url: str, output_dir: str) -> str:
    try:
        response = requests.get(url)  # create HTTP response object
        logger.info('Http response code %s', response.status_code)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()

    except HTTPError as http_err:
        raise ValueError('HTTP error occurred: {}'.format(http_err))
    except Exception as err:
        raise ValueError('Other error occurred: {}'.format(err))

    content = response.content
    logger.debug('Full http response body %s', content)
    soup = BeautifulSoup(content, 'html.parser')
    logger.debug('Parsed html body %s', soup)
    clean_url = url.strip('/')
    resulting_file_name = url_parser.format_url(clean_url, 'file')
    complete_path = os.path.join(output_dir, resulting_file_name)

    image_tags = soup.findAll('img')
    link_tags = soup.findAll('link')
    script_tags = soup.findAll('script')

    logger.debug('All img tags body %s', image_tags)
    logger.debug('All link tags %s', link_tags)
    logger.debug('All script %s', script_tags)

    download_res(clean_url, output_dir, image_tags)
    download_res(clean_url, output_dir, link_tags, 'href')
    download_res(clean_url, output_dir, script_tags)

    try:
        with open(complete_path, "w", encoding='utf-8') as file:
            file.write(str(soup.prettify()))
            logger.info('Successfully save file %s', complete_path)
        return complete_path
    except OSError:
        logger.error('Failed to write data into %s', complete_path)
        raise ValueError("Directory is not available.")


def download_res(url: str, output_dir: str, tags: list, location: str = 'src'):
    dir_name = url_parser.format_url(url, 'dir')
    dir_full_path = os.path.join(output_dir, dir_name)
    if not os.path.exists(dir_full_path):
        try:
            os.mkdir(dir_full_path)
            logger.info('Successfully created directory %s', dir_full_path)
        except OSError:
            logger.error('Failed to write data into %s', dir_full_path)
            raise ValueError("Directory is not available.")

    for tag in tags:
        if not url_parser.check_domain(url, tag.get(location)):
            continue

        link = urljoin(url, tag.get(location))
        res_name = url_parser.format_url(link, 'file')
        full_file_path = '{}/{}'.format(dir_full_path, res_name)
        res_file_path = '{}/{}'.format(dir_name, res_name)
        tag[location] = res_file_path
        with requests.get(link, stream=True) as r:
            r.raise_for_status()
            logger.info('Saving file %s', full_file_path)
            with open(full_file_path, 'wb') as file:
                for chunk in r.iter_content(chunk_size=8192):
                    file.write(chunk)
