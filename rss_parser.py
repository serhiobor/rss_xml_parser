from typing import List, Optional
from collections import OrderedDict
import re


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
    def get_feed_info(xml_string):
        feed_elem_ord = ['title',
                         'link',
                         'lastBuildDate',
                         'pubDate',
                         'language',
                         'category',
                         'managinEditor',
                         'description',
                         'item']
        feed_regex = "<channel>(.*?)<item>"
        feed_string = re.findall(feed_regex, xml_string, flags=re.DOTALL)[0]
        feed_tags_dict = OrderedDict()
        for tag in feed_elem_ord:
            tag_regex = f"<({tag})>(?P<{tag}>.*)</({tag})>"
            value = re.search(tag_regex, feed_string)
            if value:
                feed_tags_dict[tag] = value.group(tag)
        return feed_tags_dict

    return get_feed_info(xml)
