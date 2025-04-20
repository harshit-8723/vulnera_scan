from scrapy.crawler import CrawlerRunner
from app.spiders.website_spider import WebsiteSpider
from scrapy.utils.project import get_project_settings
from scrapy.utils.defer import deferred_to_future
import asyncio
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

class CustomCrawler:
    def __init__(self, target_url : str, timeout : float = 30.0):
        logger.info(f"Initializing CustomCrawler for URL: {target_url} with timeout: {timeout}")
        self.target_url = target_url
        self.found_urls = set()
        # additional logic for timeout after how much seconds
        self.timeout = timeout

    async def run(self):
        logger.info(f"Starting crawl for URL: {self.target_url}")
        # configure Scrapy settings
        settings = get_project_settings()
        settings.update({
            "LOG_ENABLED": True,
            "LOG_LEVEL": "INFO", # sets the log level 
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "DOWNLOAD_DELAY": 1.0,  # avoid overloading server
            "CONCURRENT_REQUESTS": 4  # balance speed and stability
        })
        
        # initializeing the crawler runner
        runner = CrawlerRunner(settings)

        # callback to collect urls;
        def collect_urls(item, response, spider):
            url = item["url"]
            self.found_urls.add(url)
            logger.info(f"Collected URL: {url}")

        #configure and run the spider
        try :
            # twisted deferred
            async with asyncio.timeout(self.timeout):
                crawl = runner.crawl(
                    WebsiteSpider,
                    start_url = self.target_url,
                    callback = collect_urls
                )
                logger.info(f"Started crawling {self.target_url}")
                #converting the deferred to asyncio for future and await it
                #wait for the crawl to complete
                await deferred_to_future(crawl)
                logger.info(f"Crawl completed for {self.target_url}, collected {len(self.found_urls)} URLs")
        except TimeoutError :
            logger.warning(f"Timeout occurred for {self.target_url}, returning {len(self.found_urls)} URLs collected so far")
            #Timeout occurred, return url collected so far
            pass
        except Exception as e:
            logger.error(f"Scrapy crawl failed for {self.target_url}: {str(e)}")
            raise RuntimeError(f"Scrapy crawl failed : {str(e)}")
        
        return self.found_urls