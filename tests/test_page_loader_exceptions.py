# -*- coding:utf-8 -*-

"""Various page_loader tests."""

import pytest
import page_loader
import requests
from page_loader.errors import FileError, NetworkError


def test_page_loader(requests_mock):
    url_normal = 'http://example.com'
    url_abnormal = 'http://unexisting.com'
    requests_mock.get(url_normal)
    requests_mock.get(url_abnormal, exc=requests.exceptions.ConnectTimeout)
    with pytest.raises(FileError):
        page_loader.download(url_normal, '/tmp1')
    with pytest.raises(NetworkError):
        page_loader.download(url_abnormal, '/tmp1')
