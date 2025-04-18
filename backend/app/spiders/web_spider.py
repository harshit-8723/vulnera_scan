import scrapy
from scrapy.http import FormRequest, Request, Response
from urllib.parse import urljoin, parse_qs, urlencode
import logging
import time

logger = logging.getLogger(__name__)

class WebsiteSpider(scrapy.Spider):
    name = "website_spider"
    allowed_domains = []
    start_urls = []
    sql_vulnerabilities = []
    xss_vulnerabilities = []

    def __init__(self, start_url, sql_payloads, xss_payloads, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [str(start_url)]
        self.allowed_domains = [str(start_url).split("//")[-1].split("/")[0]]
        self.sql_payloads = sql_payloads
        self.xss_payloads = xss_payloads
        self.visited_urls = set()

    def parse(self, response: Response):
        self.visited_urls.add(response.url)

        # Step 1: Test query parameters in the current URL
        yield from self.test_query_parameters(response.url)

        # Step 2: Extract and test forms
        forms = response.xpath("//form")
        for form in forms:
            action = form.xpath("@action").get() or response.url
            method = form.xpath("@method").get(default="get").lower()
            inputs = form.xpath(".//input | .//textarea | .//select")
            form_data = {}
            for input_field in inputs:
                name = input_field.xpath("@name").get()
                if name:
                    form_data[name] = ""

            if form_data:
                absolute_action = urljoin(response.url, action)
                yield from self.test_form(absolute_action, method, form_data, response.url)

        # Step 3: Extract URLs for crawling
        links = response.xpath("//a/@href").getall()
        for link in links:
            absolute_url = urljoin(response.url, link)
            if absolute_url not in self.visited_urls and self.allowed_domains[0] in absolute_url:
                yield scrapy.Request(absolute_url, callback=self.parse)

    def test_query_parameters(self, url):
        # Parse query parameters from the URL
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        logger.debug(f"Found query parameters in {url}: {query_params}")
        if not query_params:
            logger.debug(f"No query parameters found in {url}")
            return

        # Base URL without query parameters
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        # Test SQL injection
        for param in query_params:
            for payload in self.sql_payloads:
                # Create a new query string with the payload
                new_params = {k: v for k, v in query_params.items()}
                new_params[param] = payload
                new_query = urlencode({k: v[0] if isinstance(v, list) else v for k, v in new_params.items()}, doseq=True)
                test_url = f"{base_url}?{new_query}"
                start_time = time.time()
                yield Request(
                    url=test_url,
                    callback=self.check_sql_response,
                    meta={"payload": payload, "field": param, "source_url": url, "start_time": start_time}
                )

        # Test XSS
        for param in query_params:
            for payload in self.xss_payloads:
                new_params = {k: v for k, v in query_params.items()}
                new_params[param] = payload
                new_query = urlencode({k: v[0] if isinstance(v, list) else v for k, v in new_params.items()}, doseq=True)
                test_url = f"{base_url}?{new_query}"
                yield Request(
                    url=test_url,
                    callback=self.check_xss_response,
                    meta={"payload": payload, "field": param, "source_url": url}
                )

    ##########################
    # def test_form(self, action, method, form_data, source_url):
    #     # Test SQL injection
    #     for payload in self.sql_payloads:
    #         for key in form_data:
    #             test_data = form_data.copy()
    #             test_data[key] = payload
    #             start_time = time.time()
    #             yield FormRequest(
    #                 url=action,
    #                 method=method,
    #                 formdata=test_data,
    #                 callback=self.check_sql_response,
    #                 meta={"payload": payload, "field": key, "source_url": source_url, "start_time": start_time}
    #             )

    #     # Test XSS
    #     for payload in self.xss_payloads:
    #         for key in form_data:
    #             test_data = form_data.copy()
    #             test_data[key] = payload
    #             yield FormRequest(
    #                 url=action,
    #                 method=method,
    #                 formdata=test_data,
    #                 callback=self.check_xss_response,
    #                 meta={"payload": payload, "field": key, "source_url": source_url}
    #             )
    ############################################

    # for testing purpose 
    def test_form(self, action, method, form_data, source_url):
        logger.debug(f"Testing form at {source_url} with action {action}, method {method}, fields {list(form_data.keys())}")
        # Test SQL injection (limit to first 5 payloads for testing)
        for payload in self.sql_payloads[:5]:  # Temporary limit for debugging
            for key in form_data:
                test_data = form_data.copy()
                test_data[key] = payload
                start_time = time.time()
                yield FormRequest(
                    url=action,
                    method=method,
                    formdata=test_data,
                    callback=self.check_sql_response,
                    meta={"payload": payload, "field": key, "source_url": source_url, "start_time": start_time}
                )

        # Test XSS (limit to first 5 payloads for testing)
        for payload in self.xss_payloads[:5]:  # Temporary limit for debugging
            for key in form_data:
                test_data = form_data.copy()
                test_data[key] = payload
                yield FormRequest(
                    url=action,
                    method=method,
                    formdata=test_data,
                    callback=self.check_xss_response,
                    meta={"payload": payload, "field": key, "source_url": source_url}
                )
        #####################

    def check_sql_response(self, response: Response):
        payload = response.meta["payload"]
        field = response.meta["field"]
        source_url = response.meta["source_url"]
        start_time = response.meta["start_time"]
        response_time = time.time() - start_time

        logger.debug(f"Checking SQL response for payload '{payload}' in '{field}' at {source_url}")
        if any(error in response.text.lower() for error in ["sql syntax", "mysql", "database error", "unexpected", "error in your sql"]):
            logger.info(f"Found SQL vulnerability: Error-based SQL Injection in '{field}' with payload '{payload}' at {source_url}")
            self.sql_vulnerabilities.append(
                f"Error-based SQL Injection in '{field}' with payload '{payload}' at {source_url}"
            )
        elif "true" in response.text.lower() and "false" not in response.text.lower():
            logger.info(f"Found SQL vulnerability: Boolean-based SQL Injection in '{field}' with payload '{payload}' at {source_url}")
            self.sql_vulnerabilities.append(
                f"Boolean-based SQL Injection in '{field}' with payload '{payload}' at {source_url}"
            )
        elif "SLEEP" in payload and response_time > 4:
            logger.info(f"Found SQL vulnerability: Time-based SQL Injection in '{field}' with payload '{payload}' at {source_url}")
            self.sql_vulnerabilities.append(
                f"Time-based SQL Injection in '{field}' with payload '{payload}' at {source_url}"
            )
        else:
            logger.debug(f"No SQL vulnerability detected for payload '{payload}' in '{field}' at {source_url}")

    def check_xss_response(self, response: Response):
        payload = response.meta["payload"]
        field = response.meta["field"]
        source_url = response.meta["source_url"]
        logger.debug(f"Checking XSS response for payload '{payload}' in '{field}' at {source_url}")
        if payload in response.text or any(keyword in response.text.lower() for keyword in ["alert(", "prompt("]):
            logger.info(f"Found XSS vulnerability: XSS in '{field}' with payload '{payload}' at {source_url}")
            self.xss_vulnerabilities.append(
                f"XSS in '{field}' with payload '{payload}' at {source_url}"
            )
        else:
            logger.debug(f"No XSS vulnerability detected for payload '{payload}' in '{field}' at {source_url}")