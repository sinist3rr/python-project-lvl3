# -*- coding:utf-8 -*-

"""Various page_loader tests."""

import pytest
import page_loader
from page_loader.errors import AppInternalError


def test_page_loader():
    with pytest.raises(AppInternalError):
        page_loader.download('http://example.com', '/tmp1')
    with pytest.raises(AppInternalError):
        page_loader.download('https://httpbin11.org/', '/tmp')
