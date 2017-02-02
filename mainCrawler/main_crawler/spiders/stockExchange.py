import scrapy
import sys

class QuotesSpider(scrapy.Spider):
    name = "stockExchange"

    # https://doc.scrapy.org/en/1.3/intro/tutorial.html#using-spider-arguments
    # scrapy crawl quotes -o quotes-humor.json -a tag=humor

    def start_requests(self):
        urlShanghai = 'http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate=2017-01-26&prodType=gp&_=1485967505892'
        urlShenzhen = 'http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.4397416552090172'

        market = getattr(self, 'market', None)
        
        if market is not None:
	        yield scrapy.Request(urlShanghai, self.parseShanghai)
	        yield scrapy.Request(urlShenzhen, self.parseShenzhen)
        if market == 'shanghai':
	        yield scrapy.Request(urlShanghai, self.parseShanghai)
        if market == 'shenzhen':
	        yield scrapy.Request(urlShenzhen, self.parseShenzhen)
        	

    # 数据源: http://www.sse.com.cn/market/stockdata/overview/day/?&lan=cn&lan=cn&lan=cn
    def parseShanghai(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    # 数据源: http://www.szse.cn/main/marketdata/tjsj/jyjg/
    # 
	def parseShenzhen(self, response):
		pass