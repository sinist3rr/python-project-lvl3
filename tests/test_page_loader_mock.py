# -*- coding:utf-8 -*-

"""Various page_loader tests."""

import pytest
import requests
import tempfile
import os
import page_loader


def test_url(requests_mock):
    with open('tests/fixtures/example-com.html') as fp:
        result_file = fp.read()

    requests_mock.get('http://example.com', text=result_file)
    page_loader.download('http://example.com', '/tmp/')

    with open('/tmp/example-com.html') as fp2:
        test_file = fp2.read()

    assert test_file == result_file

