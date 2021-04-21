import os
import logging
import page_loader.page_parser
import page_loader.resource_handler
import page_loader.url_parser


logger = logging.getLogger(__name__)


def download(url: str, output_dir: str) -> str:
    webpage_content = page_loader.resource_handler.get_http(url)
    logger.debug('Full http response body %s', webpage_content)

    resulting_file_name = page_loader.url_parser.format_file_url(url)
    complete_path = os.path.join(output_dir, resulting_file_name)

    soup, all_tags = page_loader.page_parser.parse_resource_tags(webpage_content)
    local_tags = page_loader.page_parser.get_local_tags(all_tags, url)

    resource_urls = page_loader.page_parser.add_to_res_list(local_tags, url)
    page_loader.page_parser.change_in_soup(local_tags, url)
    if resource_urls:
        dir_full_path = page_loader.resource_handler.create_res_dir(url, output_dir)
        page_loader.resource_handler.run_download_res(dir_full_path, resource_urls)
    page_loader.resource_handler.save_result_html(soup, complete_path)
    return complete_path
