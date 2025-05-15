import httpx
import logging
import asyncio
from typing import List, Dict, AsyncGenerator
from backend.app.payloads.sql_payloads import BASIC_SQL_PAYLOADS, UNION_SQL_PAYLOADS, ERROR_SQL_PAYLOADS, TIME_SQL_PAYLOADS
from backend.app.payloads.xss_payloads import REFLECTED_XSS_PAYLOADS, STORED_XSS_PAYLOADS, DOM_XSS_PAYLOADS, ATTRIBUTE_XSS_PAYLOADS

logger = logging.getLogger(__name__)

async def test_vulnerabilities(
    urls: List[str],
    timeout: float = 60.0,
    max_urls: int = 5,
    max_payloads_per_type: int = 5
) -> AsyncGenerator[Dict, None]:
    """
    Test URLs for SQL injection and XSS vulnerabilities, yielding progress updates.
    Stops after specified timeout or tests limited URLs/payloads for quick testing.

    :param urls: List of URLs to test.
    :param timeout: Maximum duration for scanning (seconds).
    :param max_urls: Maximum number of URLs to test (0 for all).
    :param max_payloads_per_type: Maximum payloads per type (SQL/XSS, 0 for all).
    :yields: Progress updates and vulnerability results as dictionaries.
    """
    results = []
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Limit URLs
        test_urls = urls[:max_urls] if max_urls > 0 else urls
        yield {"event": "progress", "message": f"Starting vulnerability scan for {len(test_urls)} URLs"}

        try:
            # Wrap scanning in timeout
            await asyncio.wait_for(
                _test_urls(test_urls, client, max_payloads_per_type, results),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            yield {"event": "progress", "message": f"Scanner stopped due to timeout after {timeout} seconds, tested {len(results)} payloads"}
        except Exception as e:
            yield {"event": "error", "message": f"Scanner error: {str(e)}"}

        # Yield final results
        for result in results:
            yield {"event": "result", "data": result}

async def _test_urls(
    urls: List[str],
    client: httpx.AsyncClient,
    max_payloads_per_type: int,
    results: List[Dict]
) -> AsyncGenerator[Dict, None]:
    """
    Helper to test URLs with payloads, yielding progress updates.
    """
    for url in urls:
        # Skip URLs unlikely to have parameters
        if not any(ext in url for ext in [".php", ".html", "?"]):
            yield {"event": "progress", "message": f"Skipping URL without parameters: {url}"}
            continue

        yield {"event": "progress", "message": f"Testing URL: {url}"}

        # Test SQL injection
        sql_payloads = (
            (BASIC_SQL_PAYLOADS[:max_payloads_per_type] if max_payloads_per_type > 0 else BASIC_SQL_PAYLOADS) +
            (UNION_SQL_PAYLOADS[:max_payloads_per_type] if max_payloads_per_type > 0 else UNION_SQL_PAYLOADS) +
            (ERROR_SQL_PAYLOADS[:max_payloads_per_type] if max_payloads_per_type > 0 else ERROR_SQL_PAYLOADS) +
            (TIME_SQL_PAYLOADS[:max_payloads_per_type] if max_payloads_per_type > 0 else TIME_SQL_PAYLOADS)
        )
        for payload in sql_payloads:
            yield {"event": "progress", "message": f"Testing {url} with SQL payload: {payload}"}
            result = await test_sql_injection(url, payload, client)
            results.append(result)
            if result["found"]:
                yield {"event": "result", "data": result}

        # Test XSS
        xss_payloads = (
            (REFLECTED_XSS_PAYLOADS[:max_payloads_per_type] if max_payloads_per_type > 0 else REFLECTED_XSS_PAYLOADS) +
            (STORED_XSS_PAYLOADS[:max_payloads_per_type] if max_payloads_per_type > 0 else STORED_XSS_PAYLOADS) +
            (DOM_XSS_PAYLOADS[:max_payloads_per_type] if max_payloads_per_type > 0 else DOM_XSS_PAYLOADS) +
            (ATTRIBUTE_XSS_PAYLOADS[:max_payloads_per_type] if max_payloads_per_type > 0 else ATTRIBUTE_XSS_PAYLOADS)
        )
        for payload in xss_payloads:
            yield {"event": "progress", "message": f"Testing {url} with XSS payload: {payload}"}
            result = await test_xss(url, payload, client)
            results.append(result)
            if result["found"]:
                yield {"event": "result", "data": result}

async def test_sql_injection(url: str, payload: str, client: httpx.AsyncClient) -> Dict:
    """
    Test a URL for SQL injection with a given payload.
    """
    result = {"url": url, "payload": payload, "vulnerability": "SQL Injection", "found": False}
    try:
        test_url = f"{url}?input={payload}" if "?" not in url else f"{url}&input={payload}"
        response = await client.get(test_url)
        if any(error in response.text.lower() for error in [
            "error in your sql syntax", "syntax error at or near",
            "incorrect syntax near", "unclosed quotation mark"
        ]):
            result["found"] = True
            logger.info(f"SQL injection detected at {url} with payload: {payload}")
        elif "SLEEP(" in payload or "WAITFOR DELAY" in payload:
            if response.elapsed.total_seconds() > 5:
                result["found"] = True
                logger.info(f"SQL injection (time-based) detected at {url} with payload: {payload}")
    except httpx.HTTPError as e:
        logger.warning(f"Error testing {url} with SQL payload {payload}: {e}")
    return result

async def test_xss(url: str, payload: str, client: httpx.AsyncClient) -> Dict:
    """
    Test a URL for XSS with a given payload.
    """
    result = {"url": url, "payload": payload, "vulnerability": "XSS", "found": False}
    try:
        test_url = f"{url}?input={payload}" if "?" not in url else f"{url}&input={payload}"
        response = await client.get(test_url)
        if payload in response.text:
            result["found"] = True
            logger.info(f"XSS detected at {url} with payload: {payload}")
    except httpx.HTTPError as e:
        logger.warning(f"Error testing {url} with XSS payload {payload}: {e}")
    return result