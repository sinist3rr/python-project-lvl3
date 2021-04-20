# -*- coding:utf-8 -*-

"""Various page_loader tests."""

import pytest
import os
import glob
import filecmp
import requests
import page_loader
from bs4 import BeautifulSoup
from page_loader.errors import FileError, NetworkError


@pytest.mark.parametrize(
    'url,result',
    [
        (
            'http://example.com',
            'example-com.html'
        ),
        (
            'https://httpbin.org/html',
            'httpbin-org-html.html'
        ),
        (
            'http://example.com/index.html',
            'example-com-index.html'
        )]
)
def test_page_loader_basic(requests_mock, tmpdir, url, result):
    filepath = 'tests/fixtures/{}'.format(result)
    with open(filepath) as fp:
        result_file = fp.read()

    requests_mock.get(url, text=result_file)
    tmp_path = page_loader.download(url, tmpdir)
    with open(tmp_path) as tmp_html_file:
        tmp_html_result_file = tmp_html_file.read()

    assert tmp_html_result_file == result_file
    assert tmp_path == os.path.join(tmpdir, result)


def test_page_loader_resources(requests_mock, tmpdir):
    url = 'https://digital.ai/devops-tool-chest/open-source'
    res_path = 'digital-ai-devops-tool-chest-open-source_files/digital-ai-devops-tool-chest-'
    images = glob.glob('tests/fixtures/img/*.png')
    css = glob.glob('tests/fixtures/css/*.css')
    js = glob.glob('tests/fixtures/js/*.js')
    resources = images + css + js

    with open('tests/fixtures/digital-ai-img-before.html') as fp:
        original_file = fp.read()
    with open('tests/fixtures/digital-ai-img-after.html') as fp:
        result_file = fp.read()
    soup = BeautifulSoup(result_file, 'html.parser')
    requests_mock.get(url, text=original_file)

    for res in resources:
        res_filename = os.path.basename(res)
        res_type = os.path.basename(os.path.dirname(res))
        with open(res, "rb") as r:
            res_file = r.read()
            requests_mock.get('https://digital.ai/devops-tool-chest/{}/{}'.format(res_type, res_filename),
                              content=res_file
                              )

    tmp_path = page_loader.download(url, tmpdir)

    for res in resources:
        res_filename = os.path.basename(res)
        res_type = os.path.basename(os.path.dirname(res))
        assert filecmp.cmp(res, '{}/{}{}-{}'.format(tmpdir, res_path, res_type, res_filename),
                           shallow=False
                           )

    with open(tmp_path) as tmp_html_file:
        tmp_html_result_file = tmp_html_file.read()

    assert tmp_html_result_file == str(soup.prettify(formatter='html5'))


def get_resource_names(resources):
    resource_names = []
    for res in resources:
        res_filename = os.path.basename(res)
        rtype = os.path.basename(os.path.dirname(res))
        resource_names.append((res, res_filename, rtype))
    return resource_names


@pytest.mark.parametrize(
    'url,text,code',
    [
        (
            'https://httpbin.org/status/403',
            'Forbidden',
            403
        ),
        (
            'https://httpbin.org/status/404',
            'Not Found',
            404
        ),
        (
            'https://httpbin.org/status/500',
            'Internal Server Error',
            500
        )]
)
def test_page_loader_codes(requests_mock, tmpdir, url, text, code):
    requests_mock.get(url, text=text, status_code=code)
    with pytest.raises(NetworkError):
        page_loader.download(url, tmpdir)


@pytest.mark.parametrize(
    'url,exception',
    [
        (
            'https://unexisting.com',
            requests.exceptions.ConnectTimeout
        ),
        (
            'https://unexisting.com',
            requests.exceptions.ConnectionError
        ),
        (
            'https://example.com',
            requests.exceptions.HTTPError
        )]
)
def test_page_loader_network(requests_mock, tmpdir, url, exception):
    requests_mock.get(url, exc=exception)
    with pytest.raises(NetworkError):
        page_loader.download(url, tmpdir)


def test_page_loader_fs(requests_mock):
    url = 'http://example.com'
    requests_mock.get(url)
    with pytest.raises(FileError):
        page_loader.download(url, '/tmp1')
