import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    rules = (
        Rule(LinkExtractor(restrict_css="ul.pager li.next a"), follow=True),
        Rule(LinkExtractor(restrict_css="h3 a"), callback="parse_book"),
    )

    def parse_book(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        def extract_rating():
            classes = response.css("p.star-rating::attr(class)").get("")
            return classes.replace("star-rating", "").strip()

        yield {
            "title": extract_with_css("h1::text"),
            "price": extract_with_css("p.price_color::text"),
            "amount_in_stock": extract_with_css("p.instock.availability::text"),
            "rating": extract_rating(),
            "category": extract_with_css("ul.breadcrumb li:nth-child(3) a::text"),
            "description": extract_with_css("meta[name='description']::attr(content)"),
            "upc": response.xpath("//th[text()='UPC']/following-sibling::td/text()").get()
        }
