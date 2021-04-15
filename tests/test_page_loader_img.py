# -*- coding:utf-8 -*-

"""Various page_loader tests."""

import tempfile
import filecmp
import page_loader
from bs4 import BeautifulSoup


def test_page_loader(requests_mock):
    url = 'https://digital.ai/devops-tool-chest/open-source'
    img_path = 'digital-ai-devops-tool-chest-open-source_files/digital-ai-devops-tool-chest-img-'
    css_path = 'digital-ai-devops-tool-chest-open-source_files/digital-ai-css-css-Tz2Slcsk93w.css'
    js_path = 'digital-ai-devops-tool-chest-open-source_files/digital-ai-js-js-Foa5XQDLxY.js'
    images = (
        'docker.png',
        'git.png',
        'gitlab.png',
        'github.png',
        'kubernetes.png',
        'terraform.png',
        'vagrant.png'
    )
    resources = ('css/css_Tz2Slcsk93w.css', 'js/js_Foa5XQDLxY.js')

    with open('tests/fixtures/digital-ai-img-before.html') as fp:
        original_file = fp.read()
    with open('tests/fixtures/digital-ai-img-after.html') as fp:
        result_file = fp.read()
    soup = BeautifulSoup(result_file, 'html.parser')

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        requests_mock.get(url, text=original_file)
        for image in images:
            with open('tests/fixtures/img/{}'.format(image), "rb") as im:
                img_file = im.read()
            requests_mock.get('https://digital.ai/devops-tool-chest/img/{}'.format(image), content=img_file)

        for res in resources:
            with open('tests/fixtures/{}'.format(res), "rb") as file:
                res_file = file.read()
            requests_mock.get('https://digital.ai/{}'.format(res), content=res_file)

        tmp_path = page_loader.download(url, tmp_dir_name)

        for image in images:
            assert filecmp.cmp('tests/fixtures/img/{}'.format(image),
                               '{}/{}{}'.format(tmp_dir_name, img_path, image),
                               shallow=False
                               )

        assert filecmp.cmp('tests/fixtures/css/css_Tz2Slcsk93w.css',
                           '{}/{}'.format(tmp_dir_name, css_path),
                           shallow=False
                           )
        assert filecmp.cmp('tests/fixtures/js/js_Foa5XQDLxY.js',
                           '{}/{}'.format(tmp_dir_name, js_path),
                           shallow=False
                           )

        with open(tmp_path) as tmp_html_file:
            tmp_html_result_file = tmp_html_file.read()

    assert tmp_html_result_file == str(soup.prettify(formatter='html5'))
