import httpx
import logging
from typing import List, Dict, AsyncGenerator
from app.payloads.sql_payloads import SQLI_PAYLOADS
from app.helper.payload_url import inject_payload

logger = logging.getLogger(__name__)

async def sql_vulnerability_scan(
    urls: List[str]
) -> AsyncGenerator[Dict, None]:
    logger.info(f"Received URLs for SQL scan: {urls}")
    yield {"event": "progress", "message": f"Scanning {len(urls)} URLs for SQL injection"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            async for event in _scan_sql(urls, client):
                yield event
        except Exception as e:
            yield {"event": "error", "message": f"SQL scanner error: {str(e)}"}



async def _scan_sql(
    urls: List[str],
    client: httpx.AsyncClient,
) -> AsyncGenerator[Dict, None]:
    for url in urls:
        if "?" not in url:
            yield {"event": "progress", "message": f"Skipping non-query URL: {url}"}
            continue

        yield {"event": "progress", "message": f"Testing SQL injection on: {url}"}
        for payload in SQLI_PAYLOADS:
            test_url = inject_payload(url, payload)

            try:
                response = await client.get(test_url)

                logger.info(f"Testing URL: {test_url}")
                logger.info(f"Payload used: {payload}")
                logger.info(f"Response code: {response.status_code}")
                logger.info(f"Elapsed time: {response.elapsed.total_seconds()}s")
                logger.info(f"Response snippet: {response.text[:200]}")

                #todo: for found i have to add a logic if the same payload is found in the response text 
                # then it should be true
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
                    break
                else:
                    logger.info(f"No SQL Injection found for: {test_url}")

            except httpx.HTTPError as e:
                logger.warning(f"Error testing {test_url}: {e}")
