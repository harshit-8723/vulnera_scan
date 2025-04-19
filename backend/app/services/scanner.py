from scrapy.crawler import CrawlerProcess
from app.spiders.website_spider import WebsiteSpider

class CustomCrawler:
    def __init__(self, target_url):
        self.target_url = target_url
        self.collected_urls = []

    def run(self):
        
        # configure Scrapy settings
        process = CrawlerProcess(settings={
            "LOG_ENABLED": True,
            "LOG_LEVEL": "INFO",  # keep logs clean
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "DOWNLOAD_DELAY": 1.0,  # avoid overloading server
            "CONCURRENT_REQUESTS": 4  # balance speed and stability
        })
        
        # run spider with target URL
        crawler = process.crawl(WebsiteSpider, target_url=self.target_url)
        process.start()

        # get URLs from the spider instance
        spider = crawler.spider
        self.collected_urls = spider.custom_urls
        return self.collected_urls