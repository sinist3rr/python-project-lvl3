# -*- coding:utf-8 -*-

"""Various page_loader tests."""

import pytest
import requests
import tempfile
import os
import page_loader
import re


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
def test_page_loader(requests_mock, url, result):
    filepath = 'tests/fixtures/{}'.format(result)
    with open(filepath) as fp:
        result_file = fp.read()

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        requests_mock.get(url, text=result_file)
        tmp_output = page_loader.download(url, tmp_dir_name)
        tmp_path = re.findall(r'"([^"]*)"', tmp_output)[0]
        with open(tmp_path) as tmp_html_file:
            tmp_html_result_file = tmp_html_file.read()

    assert tmp_html_result_file == result_file
    assert tmp_path == os.path.join(tmp_dir_name, result)
