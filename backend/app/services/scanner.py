from scrapy.crawler import CrawlerRunner
from app.spiders.website_spider import WebsiteSpider
import asyncio

class CustomCrawler:
    def __init__(self, target_url : str):
        self.target_url = target_url
        self.found_urls = set()

    async def run(self):
        # configure Scrapy settings
        settings = CrawlerRunner(settings={
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
        crawl = runner.crawl(
            WebsiteSpider,
            start_url = self.target_url,
            callback = collect_urls
        )

        #wait for the crawl to complete it process
        await crawl
        return self.found_urls