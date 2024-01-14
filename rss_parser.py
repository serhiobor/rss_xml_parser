from typing import List, Optional
from collections import OrderedDict
import argparse
import re
import json as jsn
import html


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json: bool = False,
) -> str:
    """
    RSS parser.

    Args:
        xml: XML document as a string.
        limit: Number of the news to return. if None, returns all news.
        json: If True, format output as JSON.

    Returns:
        Strings or JSON to console output.
    """

    def tags_to_dict(xml_string: str, tags_order: dict):
        """Make an OrderDict from xml-string where tags==keys."""
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
        """Generates string output from dicts with info"""
        string_to_output = ''
        for tag in dict_with_info:
            tag_name = order_of_tags.get(tag)
            tag_value = dict_with_info.get(tag)
            if isinstance(tag_value, list):
                tag_value = ', '.join(tag_value)
            string = f'{tag_name}{tag_value}\n'
            string_to_output += string
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

    xml = html.unescape(xml)  # remove special chars (&amp ect.)
    feed_elem_order = {
        'title': 'Feed: ',
        'link': 'Link: ',
        'lastBuildDate': 'Last Build Date: ',
        'pubDate': 'Publish Date: ',
        'language': 'Language: ',
        'category': 'Categories: ',
        'managinEditor': 'Editor: ',
        'description': 'Description: ',
        'item': 'Items:'
    }  # to formatting of feed-info output
    item_elem_order = {
        'title': 'Title: ',
        'author': 'Author: ',
        'pubDate': 'Published: ',
        'link': 'Link: ',
        'category': 'Categories: ',
        'description': '\n'
    }  # to formatting of items-info output
    xml_has_items = '<item>' in xml

    feed_regex = ("<channel>(.*?)(</channel>)", "<channel>(.*?)<item>")[
        xml_has_items]  # depends on the presence of items in xml
    feed_string = re.search(feed_regex, xml, flags=re.DOTALL).group()

    items_string = None
    if xml_has_items:
        items_string = re.split("(</*channel>)", xml)[2]

    if json:
        dict_to_output = get_feed_info()
        if xml_has_items:
            dict_to_output['items'] = get_items()
        return jsn.dumps(dict_to_output, indent=2)

    string_to_output = ''
    feed_info = get_feed_info()
    feed_string = get_output_string(feed_info, feed_elem_order)
    string_to_output += feed_string
    if xml_has_items:
        string_to_output += '\n'
        items = get_items()
        for item in items:
            item_string = '\n' + get_output_string(item, item_elem_order)
            string_to_output += item_string
            string_to_output += '\n*****\n'
    return string_to_output[:-2]


def main():
    """Main func with cli parser."""
    parser = argparse.ArgumentParser(
        prog="rss_parser",
        description="Pure Python command-line RSS reader."
    )
    parser.add_argument(
        'xml',
        type=str,
        help='file with xml string with rss info'
    )
    parser.add_argument(
        '-j', '--json',
        help="Print result as JSON in stdout",
        action='store_true'
    )
    parser.add_argument(
        '-l', '--limit',
        type=int,
        help="Limit news topics if this parameter provided",
    )
    args = parser.parse_args()
    with open(file=args.xml, encoding='utf-8', mode='r') as file:
        xml = file.read()
    try:
        print(rss_parser(xml, json=args.json, limit=args.limit))
    except Exception as e:
        raise e


if __name__ == '__main__':
    main()
