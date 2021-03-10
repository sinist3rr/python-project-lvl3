import requests
import re
import os
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup  # type: ignore
from urllib.parse import urljoin, urlparse


def download(URL: str, OUTPUT_DIR: str) -> str:
    try:
        response = requests.get(URL)  # create HTTP response object
        # If the response was successful, no Exception will be raised
        response.raise_for_status()

    except HTTPError as http_err:
        raise ValueError('HTTP error occurred: {}'.format(http_err))
    except Exception as err:
        raise ValueError('Other error occurred: {}'.format(err))

    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    resulting_file_name = format_url(URL, 'file')
    complete_path = os.path.join(OUTPUT_DIR, resulting_file_name)
    image_tags = soup.findAll('img')
    link_tags = soup.findAll('link')
    script_tags = soup.findAll('script')

    download_res(URL, OUTPUT_DIR, image_tags)
    download_res(URL, OUTPUT_DIR, link_tags, 'href')
    download_res(URL, OUTPUT_DIR, script_tags)

    try:
        with open(complete_path, "w", encoding='utf-8') as file:
            file.write(str(soup.prettify()))
        return complete_path
    except OSError:
        raise ValueError("Directory is not available.")


def download_res(URL: str, OUTPUT_DIR: str, tags: list, location: str = 'src'):
    dir_name = format_url(URL, 'dir')
    dir_full_path = os.path.join(OUTPUT_DIR, dir_name)
    if not os.path.exists(dir_full_path):
        os.mkdir(dir_full_path)

    for tag in tags:
        if check_domain(URL, tag.get(location)) and tag.get(location):
            link = urljoin(URL, tag.get(location))
            response = requests.get(link)
            res_name = format_url(link, 'file')
            full_file_path = '{}/{}'.format(dir_full_path, res_name)
            res_file_path = '{}/{}'.format(dir_name, res_name)
            tag[location] = res_file_path
            with open(full_file_path, 'wb') as file:
                file.write(response.content)
        else:
            continue


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
    main_domain = urlparse(base_url).hostname
    resource_domain = urlparse(resource_url).hostname

    if resource_domain is None or main_domain is None:
        return True
    elif resource_domain.endswith(main_domain):
        return True
    else:
        return False
