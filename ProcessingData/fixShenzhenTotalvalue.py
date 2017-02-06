# -*- coding: utf-8 -*-
import MySQLdb
import time
import sys
import MySQLdb
from lxml import etree

dbpool=MySQLdb.connect(
	host='127.0.0.1',
	db = 'stock_data',
	user = 'root',
	passwd = 'cyhcyh',
	port=3306,
	charset = 'utf8',
)
myCursor=dbpool.cursor()

myCursor.execute('SELECT backup,id FROM index_day_historical_data WHERE `type` = 399001 ')
# myCursor.execute('SELECT backup,id FROM index_day_historical_data WHERE `type` = 399001 and `date`="2015-06-05"')
resultStockList=myCursor.fetchall()

# print resultStockList
# exit()
print('-----------shenzhen---------------')
for stocklistkey in range(len(resultStockList)):
		mySelector=etree.HTML(resultStockList[stocklistkey][0])
		currDate = mySelector.xpath('//input[@id="1803_gid_tab1_con_txtQueryDate"]/@value')
		currDate = str(currDate[0])
		resultMarketValue=mySelector.xpath(u"//td[.='股票总市值（元）']/../td[2]")
		# print currDate
		# print resultMarketValue[0].text
		# exit()
		print '~~~~~~~~~~today is '+currDate
		
		if resultMarketValue==[]:
			resultMarketValue=0
		else:
			resultMarketValue=resultMarketValue[0].text
			resultMarketValue=resultMarketValue.replace(',','')


		currentStamp=str(int(time.time()))
		updateSql="UPDATE `index_day_historical_data` SET `total_value` = '"+str(resultMarketValue)+"' WHERE `type` = 399001 and `date`='"+currDate+"'"
		# print updateSql
		# exit()
		myCursor.execute(updateSql)