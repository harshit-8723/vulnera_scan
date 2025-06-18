from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from app.services.crawler import CustomCrawler
from app.helper.query_url_filter import filter_query_urls
from app.services.sql_scanner import sql_vulnerability_scan
from app.services.xss_scanner import xss_vulnerability_scan
from urllib.parse import urlparse
from app.helper.gather_recon_info import gather_recon_info
import logging
from typing import Dict
from fastapi.responses import PlainTextResponse
from app.helper.summary_generator import generate_summary_ai
from app.models.requests import SummaryRequest
from fastapi.responses import StreamingResponse
from io import BytesIO

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
origins = [
    "http://localhost:5173", 
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)



# for checking the backend
@app.get("/")
async def read_root():
    logger.info("Received request to root endpoint")
    return {"message": "Website link crawler"}


# this api endpoint scans for the SQL Injection in the url provided by the user
@app.get("/api/sql_scan")
async def sql_scan(url: str):
    logger.info(f"Received SQL scan request for URL: {url}")
    
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        logger.error(f"Invalid URL scheme for {url}")
        raise HTTPException(status_code=400, detail="Invalid URL scheme. Use http or https.")

    try:
        # first crawling the site and getting the urls
        crawler = CustomCrawler(url, timeout=30.0)
        found_urls = await crawler.run()
        logger.info(f"Crawler completed for {url}, found {len(found_urls)} URLs")

        # now filtering the url and only keeping the one with the query parameters
        query_urls = filter_query_urls(found_urls)
        logger.info(f"Filtered {len(query_urls)} URLs with query parameters")
        logger.info(f"urls ::::${query_urls}")
        

        scan_results = []
        async for event in sql_vulnerability_scan(query_urls):
            logger.info(f"events is : ${event}")
            if event.get("event") == "result":
                scan_results.append(event["data"])

        return {"url": url, "results": scan_results}
    
    except Exception as e:
        logger.error(f"SQL scan error for {url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"SQL scan error: {str(e)}")




# this api endpoint scans for the XSS Injection in the url provided by the user
@app.get("/api/xss_scan")
async def xss_scan(url: str):
    logger.info(f"Received XSS scan request for URL: {url}")

    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        logger.error(f"Invalid URL scheme for {url}")
        raise HTTPException(status_code=400, detail="Invalid URL scheme. Use http or https.")

    try:
        # first crawling the site and getting the urls
        crawler = CustomCrawler(url, timeout=30.0)
        found_urls = await crawler.run()
        logger.info(f"Crawler completed for {url}, found {len(found_urls)} URLs")

        # now filtering the url and only keeping the one with the query parameters
        query_urls = filter_query_urls(found_urls)
        logger.info(f"Filtered {len(query_urls)} URLs with query parameters")

        
        scan_results = []
        async for event in xss_vulnerability_scan(query_urls):
            if event.get("event") == "result":
                scan_results.append(event["data"])

        return {"url": url, "results": scan_results}

    except Exception as e:
        logger.error(f"XSS scan error for {url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"XSS scan error: {str(e)}")

    

# it gets the basic information of the url 
@app.get("/api/get_info")
async def get_info(url: str):
    try:
        data: Dict = await gather_recon_info(url)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.post("/api/generate_summary")
async def generate_summary(payload: SummaryRequest):
    logger.info(f"Received summary payload: {payload.model_dump()}")

    try:
        full_data = {
            "recon": payload.reconData.model_dump(),
            "sql": {
                "url": payload.sqlScanResult.url,
                "results": [r.model_dump() for r in payload.sqlScanResult.results]
            },
            "xss": {
                "url": payload.xssScanResult.url,
                "results": [r.model_dump() for r in payload.xssScanResult.results]
            }
        }

        logger.info(f"Full data is : {full_data}")

        summary_text = await generate_summary_ai(full_data)
        logger.info(f"Received information from google gemini api : {summary_text}")

        # Convert to markdown file and return
        md_file = BytesIO(summary_text.encode("utf-8"))
        return StreamingResponse(
            md_file,
            media_type="text/markdown",
            headers={"Content-Disposition": "attachment; filename=security_summary.md"}
        )

    except Exception as e:
        logger.error(f"Error in /api/generate_summary: {str(e)}")
        return PlainTextResponse(content=str(e), status_code=500)
