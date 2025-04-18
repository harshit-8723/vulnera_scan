import asyncio
import requests
from scrapy.crawler import CrawlerProcess
from app.spiders.web_spider import WebsiteSpider
from app.services.payloads import SQL_PAYLOADS, XSS_PAYLOADS
import logging

logger = logging.getLogger(__name__)

class VulnerabilityScanner:
    async def check_server_misconfiguration(self, url: str) -> list:
        vulnerabilities = []
        try:
            response = requests.get(url, timeout=5)
            headers = response.headers
            if "X-Frame-Options" not in headers:
                vulnerabilities.append("Missing X-Frame-Options header (Clickjacking risk)")
            if "Content-Security-Policy" not in headers:
                vulnerabilities.append("Missing Content-Security-Policy header")
            if "Strict-Transport-Security" not in headers:
                vulnerabilities.append("Missing HSTS header")
            if "X-Content-Type-Options" not in headers:
                vulnerabilities.append("Missing X-Content-Type-Options header")
            if "Server" in headers and any(s in headers["Server"].lower() for s in ["apache", "nginx", "iis"]):
                vulnerabilities.append(f"Server version exposed: {headers['Server']}")
            return vulnerabilities
        except Exception as e:
            logger.error(f"Error checking server misconfiguration: {e}")
            return ["Error during server misconfiguration check"]

    async def run_crawler(self, url: str) -> dict:
        # Dictionary to store results from the spider
        results = {"sql_vulnerabilities": [], "xss_vulnerabilities": []}

        # Define a callback to collect results after the spider finishes
        def configure_crawler(crawler):
            spider = crawler.spider
            results["sql_vulnerabilities"] = spider.sql_vulnerabilities
            results["xss_vulnerabilities"] = spider.xss_vulnerabilities

        process = CrawlerProcess(settings={
            "LOG_ENABLED": False,
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "DOWNLOAD_DELAY": 1.0,  # Rate-limiting
            "CONCURRENT_REQUESTS": 4,
        })

        # Pass the spider class and arguments to crawl
        process.crawl(
            WebsiteSpider,
            start_url=url,
            sql_payloads=SQL_PAYLOADS,
            xss_payloads=XSS_PAYLOADS
        )

        # Start the crawler process (synchronous)
        process.start()

        return results

    async def scan(self, url: str) -> dict:
        server_vulns = await self.check_server_misconfiguration(url)
        crawler_results = await self.run_crawler(url)
        return {
            "server_misconfiguration": server_vulns,
            "sql_injection": crawler_results["sql_vulnerabilities"],
            "xss_injection": crawler_results["xss_vulnerabilities"]
        }