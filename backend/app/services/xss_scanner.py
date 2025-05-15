import httpx
import logging
import asyncio
from typing import List, Dict, AsyncGenerator
from app.payloads.xss_payloads import XSS_PAYLOADS

logger = logging.getLogger(__name__)

async def xss_vulnerability_scan(
    urls: List[str],
    timeout: float = 60.0,
    max_urls: int = 5,
    max_payloads: int = 5
) -> AsyncGenerator[Dict, None]:
    results = []
    async with httpx.AsyncClient(timeout=10.0) as client:
        test_urls = urls[:max_urls] if max_urls > 0 else urls
        yield {"event": "progress", "message": f"Scanning {len(test_urls)} URLs for XSS"}

        try:
            await asyncio.wait_for(
                _scan_xss(test_urls, client, max_payloads, results),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            yield {"event": "progress", "message": f"Timeout after {timeout} seconds"}
        except Exception as e:
            yield {"event": "error", "message": f"XSS scanner error: {str(e)}"}

        for result in results:
            yield {"event": "result", "data": result}

async def _scan_xss(
    urls: List[str],
    client: httpx.AsyncClient,
    max_payloads: int,
    results: List[Dict]
) -> AsyncGenerator[Dict, None]:
    payloads = XSS_PAYLOADS[:max_payloads] if max_payloads > 0 else XSS_PAYLOADS

    for url in urls:
        if "?" not in url:
            yield {"event": "progress", "message": f"Skipping non-query URL: {url}"}
            continue

        yield {"event": "progress", "message": f"Testing XSS on: {url}"}
        for payload in payloads:
            test_url = url + payload
            try:
                response = await client.get(test_url)
                found = payload in response.text

                result = {
                    "url": test_url,
                    "payload": payload,
                    "vulnerability": "XSS",
                    "found": found
                }
                results.append(result)

                if found:
                    logger.info(f"XSS found at {test_url}")
                    yield {"event": "result", "data": result}

            except httpx.HTTPError as e:
                logger.warning(f"Error testing {test_url}: {e}")
