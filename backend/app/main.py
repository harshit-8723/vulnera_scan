from fastapi import FastAPI, HTTPException
from app.models.requests import WebsiteInput
from app.services.crawler import CustomCrawler
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

app = FastAPI()

@app.get("/")
async def read_root():
    logger.info("Received request to root endpoint")
    return {"message": "Website link crawler"}

@app.post("/scan")
async def scan_website(input_data: WebsiteInput):
    logger.info(f"Received scan request for URL: {input_data.url}")
    target_url = str(input_data.url)
    
    # Validate URL scheme
    parsed = urlparse(target_url)
    if not parsed.scheme in ('http', 'https'):
        logger.error(f"Invalid URL scheme for {target_url}")
        raise HTTPException(status_code=400, detail="Invalid URL scheme. Use http or https.")
    
    try:
        crawler = CustomCrawler(target_url, timeout=30.0)
        found_urls = await crawler.run()
        logger.info(f"Crawler completed for {target_url}, found {len(found_urls)} URLs")
    except Exception as e:
        logger.error(f"Crawler error for {target_url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Crawler error: {str(e)}")
    
    return {"url": target_url, "urls": found_urls}