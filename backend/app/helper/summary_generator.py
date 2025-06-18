import os
import httpx
from dotenv import load_dotenv
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

load_dotenv()

GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
GOOGLE_GEMINI_MODEL = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-1.5-flash")

# print("API Key Loaded:", GOOGLE_GEMINI_API_KEY)

GEMINI_API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GOOGLE_GEMINI_MODEL}:generateContent?key={GOOGLE_GEMINI_API_KEY}"
)

HEADERS = {"Content-Type": "application/json"}


#  this is goint to generat summary by sending teh request to google gemini
async def generate_summary_ai(data: dict) -> str:
    logger.info("reached till here in generate_summary fn")

    if not GOOGLE_GEMINI_API_KEY:
        raise RuntimeError("GOOGLE_GEMINI_API_KEY is not set.")

    user_prompt = f"""
You are a cybersecurity expert.

Using the following scan data, generate a structured **Markdown (.md)** report that includes:

## Output Format:

### 1. Executive Summary
- Provide a high-level overview of the website's security posture.

### 2. Vulnerability Analysis
- For each domain in the data:
  - Clearly list all **identified vulnerabilities** (e.g., SQLi, XSS) with:
    - Affected pages/URLs
    - Risk impact
    - Payloads used
    - Brief technical explanation

### 3. Reconnaissance Overview
- Present recon data (WHOIS, DNS, server headers, open ports) in a concise format.

### 4. Recommendations
- Actionable and prioritized recommendations for:
  - Fixing vulnerabilities
  - Hardening infrastructure
  - Any additional security best practices

### 5. Conclusion
- Emphasize the importance of continuous monitoring, and suggest tools or practices.

### Markdown Guidelines:
- Use headings (##, ###), bullet points, and code blocks (`code`) where helpful.
- Keep the report professional, concise, and easy to read.

## Input Data:
{data}
"""


    payload = {
        "contents": [{"parts": [{"text": user_prompt}]}]
    }

    logger.info("done with creating payload and prompt")

    try:
        timeout = httpx.Timeout(30.0)  # set timeout to 30 seconds
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(GEMINI_API_URL, json=payload, headers=HEADERS)
    except Exception as e:
        logger.error("Exception during Gemini API call:")
        raise RuntimeError(f"HTTPX Gemini error: {str(e)}")

    logger.info("done with the request and got the response")

    if response.status_code == 200:
        content = response.json()
        return content["candidates"][0]["content"]["parts"][0]["text"]
    else:
        logger.error("Gemini API Error: %s %s", response.status_code, response.text)
        raise RuntimeError(f"Gemini API Error: {response.status_code} - {response.text}")