# -*- coding:utf-8 -*-

"""Various page_loader tests."""

import pytest
import tempfile
import os
import page_loader


@pytest.mark.parametrize(
    'url,result',
    [
        (
            'http://example.com',
            'example-com.html'
        ),
        (
            'https://httpbin.org/html',
            'httpbin-org.html'
        ),
        (
            'http://example.com/index.html',
            'example-com-index.html'
        )]
)
def test_page_loader(url, result):
    filepath = 'tests/fixtures/{}'.format(result)
    with open(filepath) as fp:
        result_file = fp.read()

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_path = page_loader.download(url, tmp_dir_name)
        with open(tmp_path) as tmp_html_file:
            tmp_html_result_file = tmp_html_file.read()

    assert tmp_html_result_file == result_file
    assert tmp_path == os.path.join(tmp_dir_name, result)
