from fastapi import FastAPI, HTTPException
from app.models.requests import WebsiteInput 
from app.models.response import ScanResult
from app.services.scanner import CustomCrawler
from urllib.parse import urlparse

app = FastAPI()

# this is just to check whether the API is working
@app.get("/")
async def read_root():
    return {"message": "This is vulnerability scanner web tool"}

# POST endpoint that takes a URL, runs crawler, and returns links
@app.post("/scan", response_model=ScanResult)
async def scan_website(input_data: WebsiteInput):
    # target url
    target_url = str(input_data.url)  # convert HttpUrl to string
    # validate URL scheme
    parsed = urlparse(target_url)
    if not parsed.scheme in ('http', 'https'):
        raise HTTPException(status_code=400, detail="Invalid URL scheme. Use http or https.")

    # this runs the custom crawler with the given URL
    try:
        crawler = CustomCrawler(target_url, timeout = 10.0)
        found_urls = await crawler.run()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crawler error: {str(e)}")

    # For now, we just return the URLs with empty vulnerability data
    # todo:: plug in injection logic later here left 
    vulnerabilities = {url: [] for url in found_urls}

    # added this to return URLs in new field
    return ScanResult(
        url=target_url,
        vulnerabilities=vulnerabilities,
        urls=found_urls
    )