from scrapy.crawler import CrawlerRunner
from app.spiders.website_spider import WebsiteSpider
from scrapy.utils.project import get_project_settings
from scrapy.utils.defer import deferred_to_future
import asyncio

class CustomCrawler:
    def __init__(self, target_url : str, timeout : float = 30.0):
        self.target_url = target_url
        self.found_urls = set()
        # additional logic for timeout after how much seconds
        self.timeout = timeout

    async def run(self):
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
            self.found_urls.add(item["url"])

        #configure and run the spider
        try :
            # twisted deferred
            async with asyncio.timeout(self.timeout):
                crawl = runner.crawl(
                    WebsiteSpider,
                    start_url = self.target_url,
                    callback = collect_urls
                )
                #converting the deferred to asyncio for future and await it
                #wait for the crawl to complete
                await deferred_to_future(crawl)
        except TimeoutError :
            #Timeout occurred, return url collected so far
            pass
        except Exception as e:
            raise RuntimeError(f"Scrapy crawl failed : {str(e)}")
        
        return self.found_urls
