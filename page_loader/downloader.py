import os
import logging
import page_loader.parsers
import page_loader.resources
import page_loader.urls


logger = logging.getLogger(__name__)


def download(url: str, output_dir: str) -> str:
    webpage_content = page_loader.resources.get_http(url)
    logger.debug('Full http response body %s', webpage_content)

    resulting_file_name = page_loader.urls.format_file_url(url)
    complete_path = os.path.join(output_dir, resulting_file_name)

    soup, all_tags = page_loader.parsers.parse_resource_tags(webpage_content)
    local_tags = page_loader.parsers.get_local_resource_tags(all_tags, url)

    resource_urls = page_loader.parsers.get_urls_list(local_tags, url)
    page_loader.parsers.change_tags_path(local_tags, url)
    if resource_urls:
        dir_full_path = page_loader.resources.create_res_dir(url, output_dir)
        page_loader.resources.download_resources(dir_full_path, resource_urls)
    page_loader.resources.save_result_html(soup, complete_path)
    return complete_path
