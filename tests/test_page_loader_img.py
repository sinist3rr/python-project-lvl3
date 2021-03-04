# -*- coding:utf-8 -*-

"""Various page_loader tests."""

import pytest
import tempfile
import filecmp
import page_loader
from bs4 import BeautifulSoup


def test_page_loader(requests_mock):
    url = 'https://digital.ai/the-ultimate-devops-tool-chest/open-source'
    img_path = 'digital-ai-the-ultimate-devops-tool-chest-open-source_files/digital-ai-the-ultimate-devops-tool-chest-img-'
    images = (
        'Logo-Dark.png',
        'docker.png',
        'git.png',
        'gitlab.png',
        'github.png',
        'kubernetes.png',
        'terraform.png',
        'vagrant.png'
    )

    with open('tests/fixtures/digital-ai-before.html') as fp:
        original_file = fp.read()
    with open('tests/fixtures/digital-ai-after-img.html') as fp:
        result_file = fp.read()
    soup = BeautifulSoup(result_file, 'html.parser')

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        requests_mock.get(url, text=original_file)
        for image in images:
            with open('tests/fixtures/img/{}'.format(image), "rb") as im:
                img_file = im.read()
            requests_mock.get('https://digital.ai/the-ultimate-devops-tool-chest/img/{}'.format(image), content=img_file)

        tmp_path = page_loader.download(url, tmp_dir_name)

        for image in images:
            assert filecmp.cmp('tests/fixtures/img/{}'.format(image),
                               '{}/{}{}'.format(tmp_dir_name, img_path, image),
                               shallow=False
                               )

        with open(tmp_path) as tmp_html_file:
            tmp_html_result_file = tmp_html_file.read()

    assert tmp_html_result_file == str(soup.prettify())
