from typing import List, Optional
from collections import OrderedDict
import re
import json as jsn
import requests
import pprint

yahoo_test = requests.get('https://news.yahoo.com/rss/').text
test = '''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">

<channel>
  <title>Feed title</title>
  <link>https://www.w3schools.com</link>
  <description>Free web building & tutorials</description>
  <item>
    <title>RSS Tutorial</title>
    <link>https://www.w3schools.com/xml/xml_rss.asp</link>
    <description>New RSS tutorial on W3Schools</description>
  </item>
  <item>
    <title>XML Tutorial</title>
    <link>https://www.w3schools.com/xml</link>
    <description>New XML tutorial on W3Schools</description>
  </item>
</channel>

</rss>'''


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

    feed_regex = "<channel>(.*?)<item>"
    feed_string = re.findall(feed_regex, xml, flags=re.DOTALL)[0]
    items_string = re.split("(</*channel>)", xml)[2]

    def tags_to_dict(xml_string: str, tags_order):
        tags_dict = OrderedDict()
        for tag in tags_order:
            tag_regex = f"<({tag})>(?P<{tag}>.*)</({tag})>"
            value = re.search(tag_regex, xml_string)
            if value:
                tags_dict[tag] = value.group(tag)
        return tags_dict

    def get_feed_info():
        feed_elem_order = ['title',
                           'link',
                           'lastBuildDate',
                           'pubDate',
                           'language',
                           'category',
                           'managinEditor',
                           'description',
                           'item']
        return tags_to_dict(feed_string, feed_elem_order)

    def get_items():
        item_elem_order = ['title',
                           'author',
                           'pubDate',
                           'link',
                           'category',
                           'description']
        items_list = items_string.split('<item>')[1:]
        list_of_items_dict = []
        for item in items_list:
            list_of_items_dict.append(tags_to_dict(item, item_elem_order))
        return list_of_items_dict

    if json:
        dict_to_output = get_feed_info()
        dict_to_output['items'] = get_items()
        return jsn.dumps(dict_to_output, indent=3)


print(rss_parser(yahoo_test, json=True))
