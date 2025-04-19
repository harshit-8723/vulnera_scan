import scrapy
from urllib.parse import urljoin

class WebsiteSpider(scrapy.Spider):
    name = "website_spider"
    # allowed domains is important as while scrapying we don't
    # want our spider to go to some other website as one website
    # might be linked to other website and it could result in 
    # scrapying many websites 
    allowed_domains = []
    # start url represents the start url of our spider from where
    # it shoudl start scrapying 
    start_urls = []

    # visited set to store links
    visited_links = set()
    # added this to store all URLs for returning to scanner
    custom_urls = []

    def __init__(self, target_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if target_url:
            self.start_urls = [str(target_url)]
            self.allowed_domains = [str(target_url).split("//")[-1].split("/")[0]]
        # initialize lists for URLs
        self.visited_links = set()
        self.custom_urls = []

    # function that will be called when the response comes back
    def parse(self, response):
        # this gets all the anchor tag and go to href and get all 
        # the links from there and gives an array 
        all_links = response.css("a::attr(href)").getall()
        
        for link in all_links:
            absolute_url = response.urljoin(link)
            # self is written as variables that belong to the class must be accessed though self
            if absolute_url in self.visited_links: 
                continue
            self.visited_links.add(absolute_url)
            self.custom_urls.append(absolute_url)

            # used yield here so that scrapy follows the these links too
            yield response.follow(link, callback=self.parse)

        # added this to collect form action URLs
        forms = response.xpath("//form/@action").getall()
        for form_action in forms:
            absolute_form_url = urljoin(response.url, form_action)
            if absolute_form_url not in self.visited_links:
                self.visited_links.add(absolute_form_url)
                self.custom_urls.append(absolute_form_url)