import scrapy


class WebsiteSpiderSpider(scrapy.Spider):
    name = "website_spider"
    # allowed domains is important as while scrapying we don't
    # want our spider to go to some other website as one website
    # might be linked to other website and it could result in 
    # scrapying many websites 
    allowed_domains = ["testphp.vulnweb.com"]
    # start url represents the start url of our spider from where
    # it shoudl start scrapying 
    start_urls = ["http://testphp.vulnweb.com/"]

    # function that will be called when the response comes back
    def parse(self, response):
        # this gets all the anchor tag and go to href and get all 
        # the links from there and gives an array 
        all_links = response.css("a::attr(href)").getall();
        
        for link in all_links : 
            yield {
                "url" : link
            }

