# -*- coding:utf-8 -*-

"""Various page_loader tests."""

import pytest
import requests
import tempfile
import os
import page_loader


def test_page_loader():
    with pytest.raises(ValueError):
        page_loader.download('http://example.com', '/tmp1')
    with pytest.raises(ValueError):
        page_loader.download('https://httpbin11.org/', '/tmp')
