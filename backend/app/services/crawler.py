import asyncio
import logging
from typing import List
import httpx
from parsel import Selector
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

class CustomCrawler:
    """
    A lightweight crawler using httpx and parsel to collect URLs from a website,
    designed for integration with FastAPI.

    :param start_url: The initial URL to start crawling.
    :type start_url: str
    :param timeout: Timeout for HTTP requests and total crawl duration (in seconds).
    :type timeout: float
    """

    def __init__(self, start_url: str, timeout: float):
        self.start_url = start_url
        self.timeout = timeout
        self.found_urls: List[str] = []
        self.visited_urls: set[str] = set()
        self.domain = urlparse(start_url).netloc

    async def run(self) -> List[str]:
        """
        Run the crawler asynchronously to collect URLs from the start URL.

        The crawl stops after the specified timeout duration, returning URLs collected
        up to that point.

        :return: A list of unique URLs found within the same domain.
        :rtype: List[str]
        :raises Exception: If the crawl fails due to network or parsing errors.
        """
        logger.info(f"Starting crawler for {self.start_url}")
        
        try:
            self.found_urls = []
            self.visited_urls = set()
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Wrap the crawl in a timeout
                await asyncio.wait_for(self._crawl(client, self.start_url), timeout=self.timeout)
            logger.info(f"Crawler finished, found {len(self.found_urls)} URLs")
            return self.found_urls
            
        except asyncio.TimeoutError:
            logger.info(f"Crawler stopped due to timeout after {self.timeout} seconds, found {len(self.found_urls)} URLs")
            return self.found_urls
        except Exception as e:
            logger.error(f"Crawler failed for {self.start_url}: {str(e)}")
            raise

    async def _crawl(self, client: httpx.AsyncClient, url: str) -> None:
        """
        Crawl a single URL, extract links, and follow them recursively within the same domain.

        :param client: The httpx AsyncClient for making HTTP requests.
        :type client: httpx.AsyncClient
        :param url: The URL to crawl.
        :type url: str
        """
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        
        try:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            
            # Check Content-Type to avoid non-text responses
            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type.lower():
                logger.debug(f"Skipping non-HTML URL: {url}")
                return
            
            # Parse HTML and extract links
            selector = Selector(text=response.text)
            links = selector.css("a::attr(href)").getall()
            
            # Process links
            for link in links:
                absolute_url = urljoin(url, link)
                if urlparse(absolute_url).netloc == self.domain:
                    if absolute_url not in self.found_urls:
                        self.found_urls.append(absolute_url)
                    await self._crawl(client, absolute_url)
                    
        except httpx.HTTPError as e:
            logger.warning(f"Failed to crawl {url}: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")