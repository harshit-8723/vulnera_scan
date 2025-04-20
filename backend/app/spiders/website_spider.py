import scrapy
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WebsiteSpider(scrapy.Spider):
    name = "website_spider"
    # allowed domains is important as while scrapying we don't
    # want our spider to go to some other website as one website
    # might be linked to other website and it could result in 
    # scrapying many websites 
    allowed_domains = []
    # start url represents the start url of our spider from where
    # it shoudl start scrapying 
    start_urls = []

    # visited set to store links
    visited_links = set()
    # added this to store all URLs for returning to scanner
    custom_urls = []

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url] if start_url else []
        # urlparse().netloc is used to get name of site removing http 
        # like wikipedia.org not http://wikipedia.org
        self.allowed_domains = [urlparse(start_url).netloc] if start_url else []
        self.visited_links = set()
        logger.info(f"Initialized spider with start_url: {start_url}, allowed_domains: {self.allowed_domains}")

    # function that will be called when the response comes back
    def parse(self, response):
        logger.info(f"Parsing URL: {response.url}")
        # Extract all href attributes from anchor tags
        all_links = response.css("a::attr(href)").getall()
        for link in all_links:
            absolute_url = response.urljoin(link)
            # Skip if already visited or not in allowed domains
            if absolute_url in self.visited_links:
                logger.debug(f"Skipping already visited URL: {absolute_url}")
                continue
            self.visited_links.add(absolute_url)
            logger.info(f"Found new URL: {absolute_url}")
            yield {
                "url": absolute_url
            }
            # Follow the link for recursive crawling
            yield response.follow(
                link,
                callback=self.parse,
            )