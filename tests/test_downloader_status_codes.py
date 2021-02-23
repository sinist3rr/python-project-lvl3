# -*- coding:utf-8 -*-

"""Various page_loader tests."""

import pytest
import tempfile
import page_loader


@pytest.mark.parametrize(
    'url,result',
    [
        (
            'https://httpbin.org/status/403',
            403
        ),
        (
            'https://httpbin.org/status/404',
            404
        ),
        (
            'https://httpbin.org/status/500',
            500
        )]
)
def test_downloader_codes(url, result):
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        tmp_path = page_loader.download(url, tmp_dir_name)

    assert tmp_path == 'error was occurred. http code is {}'.format(result)
