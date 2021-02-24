import requests
from requests.exceptions import HTTPError
import re
import os


def remove_scheme(URL: str) -> str:
    pattern = re.compile(r"https?://?")
    return pattern.sub('', URL).strip().strip('/')


def replace_to_dash(string) -> str:
    pattern = re.compile('[^a-zA-Z0-9]')
    return re.sub(pattern, '-', string)


def add_extension(string) -> str:
    if string.endswith('html'):
        return '{}.html'.format(string[:-5])
    else:
        return '{}.html'.format(string)


def download(URL: str, OUTPUT_DIR: str) -> str:
    try:
        response = requests.get(URL)  # create HTTP response object
        # If the response was successful, no Exception will be raised
        response.raise_for_status()

    except HTTPError as http_err:
        raise ValueError('HTTP error occurred: {}'.format(http_err))
    except Exception as err:
        raise ValueError('Other error occurred: {}'.format(err))
    else:
        resulting_file_name = add_extension(
            replace_to_dash(
                remove_scheme(URL)
            )
        )
        complete_path = os.path.join(OUTPUT_DIR, resulting_file_name)

        try:
            with open(complete_path, 'wb') as f:
                f.write(response.content)
            return complete_path
        except OSError:
            raise ValueError("Directory is not available.")
