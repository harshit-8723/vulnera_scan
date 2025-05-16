from fastapi import FastAPI, HTTPException
from app.models.requests import WebsiteInput
from app.services.crawler import CustomCrawler
from app.helper.query_url_filter import filter_query_urls
from app.services.sql_scanner import sql_vulnerability_scan
from app.services.xss_scanner import xss_vulnerability_scan
from urllib.parse import urlparse
from app.helper.gather_recon_info import gather_recon_info
import logging
from typing import Dict

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

app = FastAPI()

@app.get("/")
async def read_root():
    logger.info("Received request to root endpoint")
    return {"message": "Website link crawler"}

@app.post("/api/sql_scan")
async def sql_scan(input_data: WebsiteInput):
    target_url = str(input_data.url)
    logger.info(f"Received SQL scan request for URL: {target_url}")
    
    parsed = urlparse(target_url)
    if parsed.scheme not in ('http', 'https'):
        logger.error(f"Invalid URL scheme for {target_url}")
        raise HTTPException(status_code=400, detail="Invalid URL scheme. Use http or https.")

    try:
        crawler = CustomCrawler(target_url, timeout=30.0)
        found_urls = await crawler.run()
        logger.info(f"Crawler completed for {target_url}, found {len(found_urls)} URLs")

        query_urls = filter_query_urls(found_urls)
        logger.info(f"Filtered {len(query_urls)} URLs with query parameters")
        for url in query_urls:
            logger.info(f"url : {url}")

        # scan_results = await scan_sql_injection(query_urls)
        # Because sql_vulnerability_scan is an async generator, you need to collect results from it:
        scan_results = []
        async for event in sql_vulnerability_scan(query_urls):
            if event.get("event") == "result":
                scan_results.append(event["data"])

        return {"url": target_url, "results": scan_results}

    except Exception as e:
        logger.error(f"SQL scan error for {target_url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"SQL scan error: {str(e)}")

@app.post("/api/xss_scan")
async def xss_scan(input_data: WebsiteInput):
    target_url = str(input_data.url)
    logger.info(f"Received XSS scan request for URL: {target_url}")

    parsed = urlparse(target_url)
    if parsed.scheme not in ('http', 'https'):
        logger.error(f"Invalid URL scheme for {target_url}")
        raise HTTPException(status_code=400, detail="Invalid URL scheme. Use http or https.")

    try:
        crawler = CustomCrawler(target_url, timeout=30.0)
        found_urls = await crawler.run()
        logger.info(f"Crawler completed for {target_url}, found {len(found_urls)} URLs")

        query_urls = filter_query_urls(found_urls)
        logger.info(f"Filtered {len(query_urls)} URLs with query parameters")

        scan_results = []
        async for event in xss_vulnerability_scan(query_urls):
            if event.get("event") == "result":
                scan_results.append(event["data"])
        return {"url": target_url, "results": scan_results}

    except Exception as e:
        logger.error(f"XSS scan error for {target_url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"XSS scan error: {str(e)}")
    

@app.get("/api/get_info")
async def get_info(url: str):
    try:
        data: Dict = await gather_recon_info(url)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))