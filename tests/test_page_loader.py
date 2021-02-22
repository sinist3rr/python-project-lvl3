# -*- coding:utf-8 -*-

"""Various page_loader tests."""

import pytest
import page_loader


@pytest.mark.parametrize(
    'url,output_dir,result',
    [
        (
            'http://example.com',
            '/tmp/',
            'example-com'
        ),
        (
            'https://ru.hexlet.io/courses',
            '/tmp/',
            'ru-hexlet-io-courses'
        ),
        (
            'http://example.com/index.html',
            '/tmp/',
            'example-com-index'
        )]
)
def test_page_loader(url, output_dir, result):
    filepath = 'tests/fixtures/{}.html'.format(result)
    with open(filepath) as fp:
        result_line = fp.read()

    assert page_loader.download(url, output_dir) == result_line
