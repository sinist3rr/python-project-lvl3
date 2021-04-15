import requests
import os
import logging
import page_loader.page_parser
import page_loader.resource_handler
from requests.exceptions import RequestException
from page_loader import url_parser  # type: ignore
from .errors import NetworkError


logger = logging.getLogger(__name__)


def download(url: str, output_dir: str) -> str:
    content = get_http(url)
    logger.debug('Full http response body %s', content)

    resulting_file_name = url_parser.format_file_url(url)
    complete_path = os.path.join(output_dir, resulting_file_name)

    soup, all_tags = page_loader.page_parser.parse_tags(content)
    local_tags = page_loader.page_parser.get_local_tags(all_tags, url)

    all_urls = page_loader.page_parser.add_to_res_list(local_tags, url)
    page_loader.page_parser.change_in_soup(local_tags, url)
    if all_urls:
        dir_full_path = page_loader.resource_handler.create_res_dir(url, output_dir)
        page_loader.resource_handler.run_download_res(dir_full_path, all_urls)
    page_loader.resource_handler.save_result_html(soup, complete_path)
    return complete_path


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
