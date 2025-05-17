import httpx
import logging
from typing import List, Dict, AsyncGenerator
from app.payloads.xss_payloads import XSS_PAYLOADS
from app.helper.payload_url import inject_payload

logger = logging.getLogger(__name__)

async def xss_vulnerability_scan(
    urls: List[str],
) -> AsyncGenerator[Dict, None]:
    test_urls = urls
    yield {"event": "progress", "message": f"Scanning {len(test_urls)} URLs for XSS"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            async for event in _scan_xss(test_urls, client):
                yield event
        except Exception as e:
            yield {"event": "error", "message": f"XSS scanner error: {str(e)}"}


async def _scan_xss(
    urls: List[str],
    client: httpx.AsyncClient,
) -> AsyncGenerator[Dict, None]:
    payloads = XSS_PAYLOADS

    for url in urls:
        if "?" not in url:
            yield {"event": "progress", "message": f"Skipping non-query URL: {url}"}
            continue

        yield {"event": "progress", "message": f"Testing XSS on: {url}"}

        for payload in payloads:
            test_url = inject_payload(url, payload)
            try:
                response = await client.get(test_url)
                logger.info(f"Testing URL: {test_url}")
                logger.info(f"Payload used: {payload}")
                logger.info(f"Response code: {response.status_code}")
                logger.info(f"Elapsed time: {response.elapsed.total_seconds()}s")
                logger.info(f"Response snippet: {response.text[:200]}")
                found = payload in response.text
                result = {
                    "url": test_url,
                    "payload": payload,
                    "vulnerability": "XSS",
                    "found": found
                }
                if found:
                    logger.info(f"XSS vulnerability found at {test_url}")
                    yield {"event": "result", "data": result}
                    break  # Stop testing more payloads for this URL
                else:
                    logger.info(f"No XSS found for: {test_url}")

            except httpx.HTTPError as e:
                logger.warning(f"Error testing {test_url}: {e}")
