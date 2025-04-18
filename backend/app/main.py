from fastapi import FastAPI, HTTPException
from app.models.requests import WebsiteInput
from app.models.response import ScanResult
from app.services.scanner import VulnerabilityScanner

# for logging 
import logging

# FastAPI app
app = FastAPI(title="Website Vulnerability Scanner")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Vulnerability scanner
scanner = VulnerabilityScanner()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/scan", response_model=ScanResult)
async def scan_website(website: WebsiteInput):
    print("here :",website)
    try:
        results = await scanner.scan(website.url)
        return ScanResult(url=website.url, vulnerabilities=results)
    except Exception as e:
        logger.error(f"Error during scan: {e}")
        raise HTTPException(status_code=500, detail="Error during vulnerability scan")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}