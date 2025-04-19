from fastapi import FastAPI, Request
from app.models.requests import WebsiteInput 
from app.models.response import ScanResult
from app.services.scanner import CustomCrawler

app = FastAPI()

# this is just to check whether the API is working
@app.get("/")
def read_root():
    return {"Hello": "World"}

# POST endpoint that takes a URL, runs crawler, and returns links
@app.post("/scan", response_model=ScanResult)
def scan_website(input_data: WebsiteInput):
    # target url
    target_url = str(input_data.url)  # convert HttpUrl to string

    # this runs the custom crawler with the given URL
    crawler = CustomCrawler(target_url)
    found_urls = crawler.run()

    # For now, we just return the URLs with empty vulnerability data
    # plug in injection logic later here left todo::
    vulnerabilities = {url: [] for url in found_urls}

    # added this to return URLs in new field
    return ScanResult(
        url=target_url,
        vulnerabilities=vulnerabilities,
        urls=found_urls
    )