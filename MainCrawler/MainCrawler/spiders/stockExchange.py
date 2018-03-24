# -*- coding: utf-8 -*-
import scrapy
# import sys
import time
import MySQLdb
import json

from MainCrawler.items import *


class StockexchangeSpider(scrapy.Spider):

	name = "stockExchange"
	# allowed_domains = ["sfds.com"]

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
	def start_requests(self):
		# urlShanghai = 'http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate=2017-01-26&prodType=gp&_=1485967505892'
		# urlShenzhen = 'http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.4397416552090172'
		self.aboutMysql()

		market = getattr(self, 'market', None)
		# print market
		resultUrl=[]

		if market=='shanghai':
			resultUrl=self.generateShanghai()
		if market == 'shenzhen':
			resultUrl=self.generateShenzhen()
		if market is None:
			# self.generateShanghai()
			# self.generateShenzhen()
			pass

		return resultUrl


	# 数据源: http://www.sse.com.cn/market/stockdata/overview/day/?&lan=cn&lan=cn&lan=cn
	def generateShanghai(self):
		shanghaiHeaders = {
			"Host":"query.sse.com.cn",
			"Referer":"http://www.sse.com.cn/market/stockdata/overview/day/?&lan=cn&lan=cn&lan=cn",
			"Connection":"keep-alive"
		}
		resultUrl=[]

		self.myCursor=self.dbpool.cursor()
		
		self.myCursor.execute("SELECT * FROM index_day_historical_data WHERE `type` = 000001")
		# self.myCursor.execute('SELECT * FROM index_day_historical_data WHERE `type` = 000001')
		resultStockList=self.myCursor.fetchall()
		# for stocklistkey in range(len(resultStockList)):
		# 	print(resultStockList[stocklistkey])
		# 	print(resultStockList[stocklistkey][1])
		# 	for stocklistkey2 in range(len(resultStockList[stocklistkey])):
		# 		print(resultStockList[stocklistkey][stocklistkey2])
		print('-----------shanghai---------------')
		for stocklistkey in range(len(resultStockList)):
			# update_time resultStockList[stocklistkey][14],total_value resultStockList[stocklistkey][12]
			if resultStockList[stocklistkey][14] is None:
				tmpUpdateTime=0
			else:
				tmpUpdateTime=resultStockList[stocklistkey][14]

			gapTimestamp=int(time.time())-tmpUpdateTime
			if resultStockList[stocklistkey][14] is None or gapTimestamp>259200 or resultStockList[stocklistkey][12]<0:
				urlShanghai='http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate='+str(resultStockList[stocklistkey][2])+'&prodType=gp&_=1485967505892'
				# urlShanghai='http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate='+'2017-01-26'+'&prodType=gp&_=1485967505892'
				# TODO 请求错误处理
				responsesss = scrapy.Request(url=urlShanghai,callback=self.indexDayParseShanghai,headers=shanghaiHeaders)
				resultUrl.append(responsesss)

		return  resultUrl

	# 数据源: http://www.szse.cn/main/marketdata/tjsj/jyjg/
	def generateShenzhen(self):
		shenzhenFormdata={
			"ACTIONID":"7",
			"AJAX":"AJAX-TRUE",
			"CATALOGID":"1803",
			"TABKEY":"tab1",
			"REPORT_ACTION":"search",
			"txtQueryDate":"",
		}
		resultUrl=[]

		self.myCursor=self.dbpool.cursor()
		
		self.myCursor.execute("SELECT * FROM index_day_historical_data WHERE `type` = 399001")
		# self.myCursor.execute("SELECT * FROM index_day_historical_data WHERE `type` = 399001")
		resultStockList=self.myCursor.fetchall()

		print('-----------shenzhen---------------')
		for stocklistkey in range(len(resultStockList)):
			# update_time resultStockList[stocklistkey][14],total_value resultStockList[stocklistkey][12]
			if resultStockList[stocklistkey][14] is None:
				tmpUpdateTime=0
			else:
				tmpUpdateTime=resultStockList[stocklistkey][14]

			gapTimestamp=int(time.time())-tmpUpdateTime
			if resultStockList[stocklistkey][14] is None or gapTimestamp>259200 or resultStockList[stocklistkey][12]<0:
				urlShenzhen='http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.5798621223025'
				# TODO 请求错误处理
				# print(str(resultStockList[stocklistkey][2]))
				shenzhenFormdata['txtQueryDate']=str(resultStockList[stocklistkey][2])
				# shenzhenFormdata['txtQueryDate']='2005-04-13'
				responsesss = scrapy.FormRequest(url=urlShenzhen,callback=self.indexDayParseShenzhen,formdata=shenzhenFormdata)
				resultUrl.append(responsesss)

		return  resultUrl

	def indexDayParseShanghai(self,response):
		print('-----------------indexDayParseShanghai------------------------')
		# resultItem=IndexDayItem()

		resJson=str(response.text[19:-1])
		resDict=json.loads(resJson)
		if resDict['result'][2]['marketValue1']=='':
			resDict['result'][2]['marketValue1']=0
		else:
			resDict['result'][2]['marketValue1']=float(resDict['result'][2]['marketValue1'])
			resDict['result'][2]['marketValue1']=resDict['result'][2]['marketValue1']*100000000

		currentStamp=str(int(time.time()))
		# print resJson
		# exit()
		
		updateSql="UPDATE `index_day_historical_data` SET `total_value` = "+str(resDict['result'][2]['marketValue1'])+",`backup` = '"+resJson+"',`update_time` = "+currentStamp+" WHERE `type` = 000001 and `date`='"+str(resDict['searchDate'])+"'"
		# print updateSql
		# exit();
		self.myCursor.execute(updateSql)

		# for resDictkey,resDictVal in resDict['result'].iteritems():
			# print resDictkey,'-fuck-',resDictVal
		# print type(resDict)
		# print resDict

		# resultItem['total_value']=resDict['result'][2]['marketValue']
		# resultItem['backup']=resJson
		# print resultItem
		# 
		# yield resultItem

	def indexDayParseShenzhen(self,response):
		print('-----------------indexDayParseShenzhen--!!------------------------')
		# old
		# currDate = response.xpath('//input[@id="1804_gid_tab1_con_txtDate"]/@value').extract()
		# currDate = str(currDate[0])
		# resultMarketValue=response.xpath('//table[@id="REPORTID_tab1"]/tr[2]/td[6]/text()').extract()

		currDate = response.xpath('//input[@id="1803_gid_tab1_con_txtQueryDate"]/@value').extract()
		currDate = str(currDate[0])
		resultMarketValue=response.xpath(u"//td[.='股票总市值（元）']/../td[2]/text()").extract()
		
		print('~~~~~~~~~~today is '+currDate)
		
		if resultMarketValue==[]:
			resultMarketValue=0
		else:
			resultMarketValue=resultMarketValue[0]
			resultMarketValue=resultMarketValue.replace(',','')

		#过滤 html,pure SB
		responseText=response.text.replace('\'','\"')

		currentStamp=str(int(time.time()))
		updateSql="UPDATE `index_day_historical_data` SET `total_value` = '"+str(resultMarketValue)+"',`backup` = '"+str(responseText)+"',`update_time` = "+currentStamp+" WHERE `type` = 399001 and `date`='"+currDate+"'"
		# print updateSql
		# exit()
		self.myCursor.execute(updateSql)