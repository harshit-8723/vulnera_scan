from typing import List
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

def filter_query_urls(urls: List[str]) -> List[str]:
    """
    Filter URLs that contain query parameters and reset the values to empty strings.
    Removes duplicate URLs.
    :param urls: List of URLs.
    :return: List of unique URLs with empty query values.
    """
    cleaned_urls = set()

    for url in urls:
        if "?" in url:
            parsed = urlparse(url)
            query_params = parse_qsl(parsed.query, keep_blank_values=True)
            if query_params:
                # Set all values to empty
                empty_query = urlencode([(key, "") for key, _ in query_params])
                cleaned = urlunparse(parsed._replace(query=empty_query))
                cleaned_urls.add(cleaned)  # add to set to remove duplicates

    return list(cleaned_urls)
