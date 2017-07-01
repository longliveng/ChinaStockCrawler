import symbol
import sys

import scrapy


# import 
class QuotesSpider(scrapy.Spider):
    name = "test1"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/'
        ]

    def parse(self, response):
        print('ffffffffff4444444ffffffffff')
        # dir(response)
        # print(response.__dict__)

        # page = response.url.split("/")
        # print(page)
        print('endddddd')
        sys.exit(0)
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


# https://doc.scrapy.org/en/1.3/intro/tutorial.html

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         'http://quotes.toscrape.com/page/1/',
#     ]

#     def parse(self, response):
#         for quote in response.css('div.quote'):
#             yield {
#                 'text': quote.css('span.text::text').extract_first(),
#                 'author': quote.css('span small::text').extract_first(),
#                 'tags': quote.css('div.tags a.tag::text').extract(),
#             }

#         next_page = response.css('li.next a::attr(href)').extract_first()
#         if next_page is not None:
#             next_page = response.urljoin(next_page)
#             yield scrapy.Request(next_page, callback=self.parse)
