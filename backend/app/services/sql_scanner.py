import httpx
import logging
from typing import List, Dict, AsyncGenerator
from app.payloads.sql_payloads import SQLI_PAYLOADS

logger = logging.getLogger(__name__)

async def sql_vulnerability_scan(
    urls: List[str],
    max_urls: int = 5,
    max_payloads: int = 5
) -> AsyncGenerator[Dict, None]:
    test_urls = urls[:max_urls] if max_urls > 0 else urls
    yield {"event": "progress", "message": f"Scanning {len(test_urls)} URLs for SQL injection"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            async for event in _scan_sql(test_urls, client, max_payloads):
                yield event
        except Exception as e:
            yield {"event": "error", "message": f"SQL scanner error: {str(e)}"}

async def _scan_sql(
    urls: List[str],
    client: httpx.AsyncClient,
    max_payloads: int
) -> AsyncGenerator[Dict, None]:
    payloads = SQLI_PAYLOADS[:max_payloads] if max_payloads > 0 else SQLI_PAYLOADS

    for url in urls:
        if "?" not in url:
            yield {"event": "progress", "message": f"Skipping non-query URL: {url}"}
            continue

        yield {"event": "progress", "message": f"Testing SQL injection on: {url}"}
        for payload in payloads:
            test_url = url + payload
            try:
                response = await client.get(test_url)

                logger.info(f"Testing URL: {test_url}")
                logger.info(f"Payload used: {payload}")
                logger.info(f"Response code: {response.status_code}")
                logger.info(f"Elapsed time: {response.elapsed.total_seconds()}s")
                logger.info(f"Response snippet: {response.text[:200]}")

                found = any(error in response.text.lower() for error in [
                    "error in your sql syntax", "syntax error at or near",
                    "incorrect syntax near", "unclosed quotation mark"
                ]) or (
                    "sleep(" in payload.lower() and response.elapsed.total_seconds() > 5
                ) or (
                    "waitfor delay" in payload.lower() and response.elapsed.total_seconds() > 5
                )

                result = {
                    "url": test_url,
                    "payload": payload,
                    "vulnerability": "SQL Injection",
                    "found": found
                }

                if found:
                    logger.info(f"SQL Injection found at {test_url}")
                    yield {"event": "result", "data": result}
                    break # stops testing further payload for this url
                else:
                    logger.info(f"No SQL Injection found for: {test_url}")

            except httpx.HTTPError as e:
                logger.warning(f"Error testing {test_url}: {e}")
