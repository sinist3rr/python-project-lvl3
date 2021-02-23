import requests
import re
import os


def remove_scheme(URL):
    pattern = re.compile(r"https?://?")
    return pattern.sub('', URL).strip().strip('/')


def replace_to_dash(string):
    pattern = re.compile('[^a-zA-Z0-9]')
    return re.sub(pattern, '-', string)


def add_extension(string):
    if string.endswith('html'):
        return '{}.html'.format(string[:-5])
    else:
        return '{}.html'.format(string)


def download(URL, OUTPUT_DIR):
    r = requests.get(URL)  # create HTTP response object
    if r.status_code == 200:
        resulting_file_name = add_extension(
            replace_to_dash(
                remove_scheme(URL)
            )
        )
        complete_path = os.path.join(OUTPUT_DIR, resulting_file_name)

        with open(complete_path, 'wb') as f:
            f.write(r.content)
        return complete_path
    else:
        return 'error was occurred. http code is {}'.format(r.status_code)
