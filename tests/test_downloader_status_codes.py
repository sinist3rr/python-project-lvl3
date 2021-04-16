# -*- coding:utf-8 -*-

"""Various page_loader tests."""

import pytest
import tempfile
import page_loader
from page_loader.errors import NetworkError


def test_downloader_codes(requests_mock):
    error_403 = 'https://httpbin.org/status/403'
    error_404 = 'https://httpbin.org/status/404'
    error_500 = 'https://httpbin.org/status/500'
    requests_mock.get(error_403, text='Forbidden', status_code=403)
    requests_mock.get(error_404, text='Not Found', status_code=404)
    requests_mock.get(error_500, text='Internal Server Error', status_code=500)
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        with pytest.raises(NetworkError):
            page_loader.download(error_403, tmp_dir_name)
            page_loader.download(error_404, tmp_dir_name)
            page_loader.download(error_500, tmp_dir_name)
