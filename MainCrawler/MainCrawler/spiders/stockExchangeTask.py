# -*- coding: utf-8 -*-
import scrapy
# import sys
import time,datetime
import MySQLdb
import json

from MainCrawler.items import *


class StockexchangetaskSpider(scrapy.Spider):

	name = "stockExchangeTask"
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
		self.now=datetime.datetime.now()

		market = getattr(self, 'market', None)
		# print market
		resultUrl=[]

		resultUrl=self.generateShanghai()
		resultUrl.extend(self.generateShenzhen())

		print resultUrl
		# exit()
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
		
		print('-----------shanghai---------------')
		for dayKey in range(5):
			gapDay=int(-dayKey)
			whereDate=self.now + datetime.timedelta(days=gapDay)
			whereDate=str(whereDate.strftime('%Y-%m-%d'))
			# whereDate='2015-06-05'
			# 
			self.myCursor.execute('SELECT * FROM index_day_historical_data WHERE `type` = 000001 and `date`="'+whereDate+'"')
			# update_time resultStock[stocklistkey][14],total_value resultStock[stocklistkey][12]
			resultStock=self.myCursor.fetchone()
			
			if resultStock is None:
			#没数据
				urlShanghai='http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate='+whereDate+'&prodType=gp&_=1485967505892'
				# urlShanghai='http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate='+'2017-01-26'+'&prodType=gp&_=1485967505892'
				# TODO 请求错误处理
				responsesss = scrapy.Request(url=urlShanghai,callback=self.indexDayParseShanghai,headers=shanghaiHeaders)
				responsesss.meta['isFirst'] = True
			else:
			#有数据
				urlShanghai='http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate='+str(resultStock[2])+'&prodType=gp&_=1485967505892'
				# urlShanghai='http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate='+'2017-01-26'+'&prodType=gp&_=1485967505892'
				# TODO 请求错误处理
				responsesss = scrapy.Request(url=urlShanghai,callback=self.indexDayParseShanghai,headers=shanghaiHeaders)
				responsesss.meta['isFirst'] = False

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
	
		
		print('-----------shenzhen---------------')
		for dayKey in range(5):
			gapDay=int(-dayKey)
			whereDate=self.now + datetime.timedelta(days=gapDay)
			whereDate=str(whereDate.strftime('%Y-%m-%d'))
			# whereDate='2015-06-05'
			# 
			self.myCursor.execute('SELECT * FROM index_day_historical_data WHERE `type` = 399001 and `date`="'+whereDate+'"')
			# update_time resultStock[stocklistkey][14],total_value resultStock[stocklistkey][12]
			resultStock=self.myCursor.fetchone()

			urlShenzhen='http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.5798621223025'
			if resultStock is None:
			#没数据
				shenzhenFormdata['txtQueryDate']=whereDate
				responsesss = scrapy.FormRequest(url=urlShenzhen,callback=self.indexDayParseShenzhen,formdata=shenzhenFormdata)
				responsesss.meta['isFirst'] = True
			else:
			#有数据
				shenzhenFormdata['txtQueryDate']=whereDate
				responsesss = scrapy.FormRequest(url=urlShenzhen,callback=self.indexDayParseShenzhen,formdata=shenzhenFormdata)
				responsesss.meta['isFirst'] = False

			resultUrl.append(responsesss)

		return  resultUrl

	def indexDayParseShanghai(self,response):
		print('-----------------indexDayParseShanghai------------------------')
		# resultItem=IndexDayItem()
		
		# print response.meta['isFirst']
		# exit()
		resJson=str(response.text[19:-1])
		resDict=json.loads(resJson)
		if resDict['result'][2]['marketValue1']=='':
			exit()
		else:
			resDict['result'][2]['marketValue1']=float(resDict['result'][2]['marketValue1'])
			resDict['result'][2]['marketValue1']=resDict['result'][2]['marketValue1']*100000000

		currentStamp=str(int(time.time()))

		if response.meta['isFirst']:
			blablaSql="INSERT INTO `index_day_historical_data`(`total_value`,`backup`,`type`,`date`,`update_time`)VALUES("+str(resDict['result'][2]['marketValue1'])+",'"+str(resJson)+"','000001','"+str(resDict['searchDate'])+"','"+currentStamp+"');"
		else:
			blablaSql="UPDATE `index_day_historical_data` SET `total_value` = "+str(resDict['result'][2]['marketValue1'])+",`backup` = '"+resJson+"',`update_time` = "+currentStamp+" WHERE `type` = 000001 and `date`='"+str(resDict['searchDate'])+"';"
		# print blablaSql
		# exit()
		self.myCursor.execute(blablaSql)


	def indexDayParseShenzhen(self,response):
		print('-----------------indexDayParseShenzhen--!!------------------------')
		# old
		# currDate = response.xpath('//input[@id="1804_gid_tab1_con_txtDate"]/@value').extract()
		# currDate = str(currDate[0])
		# resultMarketValue=response.xpath('//table[@id="REPORTID_tab1"]/tr[2]/td[6]/text()').extract()

		currDate = response.xpath('//input[@id="1803_gid_tab1_con_txtQueryDate"]/@value').extract()
		currDate = str(currDate[0])
		resultMarketValue=response.xpath(u"//td[.='股票总市值（元）']/../td[2]/text()").extract()
		
		print '~~~~~~~~~~today is '+currDate
		
		if resultMarketValue==[]:
			exit()
		else:
			resultMarketValue=resultMarketValue[0]
			resultMarketValue=resultMarketValue.replace(',','')

		#过滤 html,pure SB
		responseText=response.text.replace('\'','\"')

		currentStamp=str(int(time.time()))


		if response.meta['isFirst']:
			blablaSql="INSERT INTO `index_day_historical_data`(`total_value`,`backup`,`type`,`date`,`update_time`)VALUES("+str(resultMarketValue)+",'"+str(responseText)+"','399001','"+str(currDate)+"','"+currentStamp+"');"
		else:
			blablaSql="UPDATE `index_day_historical_data` SET `total_value` = "+str(resultMarketValue)+",`backup` = '"+responseText+"',`update_time` = "+currentStamp+" WHERE `type` = 399001 and `date`='"+str(currDate)+"';"
		# print blablaSql
		# exit()
		self.myCursor.execute(blablaSql)