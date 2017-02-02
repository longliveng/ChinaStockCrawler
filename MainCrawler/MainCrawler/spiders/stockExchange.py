# -*- coding: utf-8 -*-
import scrapy
import sys
import time
import MySQLdb


class StockexchangeSpider(scrapy.Spider):

	name = "stockExchange"
	# allowed_domains = ["sfds.com"]

	# start_urls = ['http://sfds.com/']
	def aboutMysql(self):
		self.dbpool = MySQLdb.connect(
			host='127.0.0.1',
			db = 'stock_data',
			user = 'root',
			passwd = 'cyhcyh',
			port=3306,
			charset = 'utf8',
		)


	# https://doc.scrapy.org/en/1.3/intro/tutorial.html#using-spider-arguments
	# scrapy crawl quotes -o quotes-humor.json -a tag=humor
# https://segmentfault.com/q/1010000005860042
	def start_requests(self):
		# urlShanghai = 'http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate=2017-01-26&prodType=gp&_=1485967505892'
		# urlShenzhen = 'http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.4397416552090172'

		self.aboutMysql()

		market = getattr(self, 'market', None)
		# print market

		if market=='shanghai':
			yield self.parseShanghai()
			# pass
		if market == 'shenzhen':
			self.parseShenzhen()
		if market is None:
			# yield scrapy.Request(urlShanghai, self.parseShanghai)
			# yield scrapy.Request(urlShenzhen, self.parseShenzhen)
			self.parseShanghai()
			self.parseShenzhen()


	# 数据源: http://www.sse.com.cn/market/stockdata/overview/day/?&lan=cn&lan=cn&lan=cn
	def parseShanghai(self):
		shanghaiHeaders = {
			"Host":"query.sse.com.cn",
			"Referer":"http://www.sse.com.cn/market/stockdata/overview/day/?&lan=cn&lan=cn&lan=cn",
			"Connection":"keep-alive"
		}
		print('-------------------aaaaaaaaaaaaaaaaaaaaaaaaaaagdgdfgdfg')
		for hh in range(3):
			print hh
		myCursor=self.dbpool.cursor()
		
		myCursor.execute('SELECT * FROM index_day_historical_data LIMIT 5')
		resultStockList=myCursor.fetchall()
		# for stocklistkey in range(len(resultStockList)):
		# 	print(resultStockList[stocklistkey])
		# 	print(resultStockList[stocklistkey][1])
		# 	for stocklistkey2 in range(len(resultStockList[stocklistkey])):
		# 		print(resultStockList[stocklistkey][stocklistkey2])
		# for stocklistkey in range(len(resultStockList)):
		# 	# update_time resultStockList[stocklistkey][14],total_value resultStockList[stocklistkey][12]
		# 	gapTimestamp=int(time.time())-resultStockList[stocklistkey][14]
			
		# 	if resultStockList[stocklistkey][14]==None or gapTimestamp>259200 or resultStockList[stocklistkey][12]<=0
				# 爬数据
		# for hh in range(3):
		# 	print hh

		urlShanghai='http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate=2017-01-26&prodType=gp&_=1485967505892'
		responsesss = scrapy.Request(url=urlShanghai,callback=self.testttparse,headers=shanghaiHeaders)
		return  responsesss
		# exit(0)


		# for quote in response.css('div.quote'):
		#     yield {
		#         'text': quote.css('span.text::text').extract_first(),
		#         'author': quote.css('span small::text').extract_first(),
		#         'tags': quote.css('div.tags a.tag::text').extract(),
		#     }

		# next_page = response.css('li.next a::attr(href)').extract_first()
		# if next_page is not None:
		#     next_page = response.urljoin(next_page)
		#     yield scrapy.Request(next_page, callback=self.parse)

	# 数据源: http://www.szse.cn/main/marketdata/tjsj/jyjg/
	def parseShenzhen(self):
		print('hehe')

	def testttparse(self,response):
		print('aaaaaaaaaaaaaa-------------------aaaaaaaaaaaaaaaaaaaaaaaaaaagdgdfgdfg')

		print(response.body)
		return response.body
