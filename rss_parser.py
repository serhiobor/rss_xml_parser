from typing import List, Optional
from collections import OrderedDict
import re
import json as jsn
import html


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json: bool = False,
) -> List[str]:
    """
    RSS parser.

    Args:
        xml: XML document as a string.
        limit: Number of the news to return. if None, returns all news.
        json: If True, format output as JSON.

    Returns:
        List of strings.
        Which then can be printed to stdout or written to file as a separate lines.

    Examples:
        >>> xml = '<rss><channel><title>Some RSS Channel</title><link>https://some.rss.com</link><description>Some RSS Channel</description></channel></rss>'
        >>> rss_parser(xml)
        ["Feed: Some RSS Channel",
        "Link: https://some.rss.com"]
        >>> print("\\n".join(rss_parser(xmls)))
        Feed: Some RSS Channel
        Link: https://some.rss.com
    """

    xml = html.unescape(xml)
    feed_regex = "<channel>(.*?)<item>"
    feed_string = re.findall(feed_regex, xml, flags=re.DOTALL)[0]
    items_string = re.split("(</*channel>)", xml)[2]

    feed_elem_order = {
        'title': 'Feed: ',
        'link': 'Link: ',
        'lastBuildDate': 'Last Build Date: ',
        'pubDate': 'Publish Date: ',
        'language': 'Language: ',
        # TODO: check formating of categories
        'category': 'Categories: ',
        'managinEditor': 'Editor: ',
        'description': 'Description: ',
        'item': 'Items:'
    }

    item_elem_order = {
        'title': 'Title: ',
        'author': 'Author: ',
        'pubDate': 'Published: ',
        'link': 'Link: ',
        # TODO: check formating
        'category': 'Categories: ',
        'description': '\n'
    }

    def tags_to_dict(xml_string: str, tags_order):
        tags_dict = OrderedDict()
        for tag in tags_order:
            tag_regex = f"<({tag})>(?P<{tag}>.*?)</({tag})>"
            value = re.search(tag_regex, xml_string)
            if value:
                if tag == 'category':
                    value = value.group(tag).split('/')
                    tags_dict[tag] = value
                else:
                    tags_dict[tag] = value.group(tag)
        return tags_dict

    def get_output_string(dict_with_info: OrderedDict, order_of_tags: dict):
        string_to_output = ''
        for tag in dict_with_info:
            tag_name = order_of_tags.get(tag)
            tag_value = dict_with_info.get(tag)
            if isinstance(tag_value, list):
                tag_value = ', '.join(tag_value)
            string = f'{tag_name}{tag_value}\n'
            string_to_output += string
        string_to_output += '\n'
        return string_to_output

    def get_feed_info():
        return tags_to_dict(feed_string, feed_elem_order.keys())

    def get_items():
        items_list = items_string.split('<item>')[1:]
        if limit:
            items_list = items_list[:limit]
        list_of_items_dict = []
        for item in items_list:
            list_of_items_dict.append(
                tags_to_dict(item, item_elem_order.keys()))
        return list_of_items_dict

    if json:
        dict_to_output = get_feed_info()
        dict_to_output['items'] = get_items()
        return jsn.dumps(dict_to_output, indent=2)

    else:
        string_to_output = ''

        feed_info = get_feed_info()
        feed_string = get_output_string(feed_info, feed_elem_order)
        string_to_output += feed_string

        items = get_items()
        for item in items:
            item_string = get_output_string(item, item_elem_order)
            string_to_output += item_string

        return string_to_output
