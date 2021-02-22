# -*- coding:utf-8 -*-

"""Various page_loader tests."""

import pytest
import page_loader


@pytest.mark.parametrize(
    'url,output_dir,result_line,result',
    [
        (
            'http://example.com',
            '/tmp/',
            '/tmp/example-com.html',
            'example-com'
        ),
        (
            'https://ru.hexlet.io/courses',
            '/tmp/',
            '/tmp/ru-hexlet-io-courses.html',
            'ru-hexlet-io-courses'
        ),
        (
            'http://example.com/index.html',
            '/tmp/',
            '/tmp/example-com-index.html',
            'example-com-index'
        )]
)
def test_page_loader(url, output_dir, result_line, result):
    filepath = 'tests/fixtures/{}.html'.format(result)
    # with open(filepath) as fp:
    # result_line = fp.read()

    # assert page_loader.download(url, output_dir) == result_line
    assert page_loader.download(url, output_dir) == result_line
