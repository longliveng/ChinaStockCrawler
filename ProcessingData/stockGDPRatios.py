# -*- coding: utf-8 -*-
from __future__ import division  
import MySQLdb
import sys
import MySQLdb
import json
# import time

dbpool=MySQLdb.connect(
	host='127.0.0.1',
	db = 'stock_data',
	user = 'root',
	passwd = 'cyhcyh',
	port=3306,
	charset = 'utf8',
)
myCursor=dbpool.cursor()

#GDP绝对值 单位(亿元)
gdpList={'gdp2016':744127,'gdp2015':676708,'gdp2014':635910,'gdp2013':588018.76,'gdp2012':534123.04,'gdp2011':473104.05,'gdp2010':401512.8,'gdp2009':340902.81,'gdp2008':314045.4,'gdp2007':265810.3,'gdp2006':216314.4,'gdp2005':184937.4,'gdp2004':159878.3,'gdp2003':135822.8,'gdp2002':120332.7,'gdp2001':109655.2,'gdp2000':99214.6,'gdp1999':89677.1,'gdp1998':84402.3,'gdp1997':78973,'gdp1996':71176.6,'gdp1995':60793.7,'gdp1994':48197.9,'gdp1993':35333.9,'gdp1992':26923.5,'gdp1991':21781.5}


myCursor.execute("SELECT `date`,sum(`total_value`) AS total_value2 FROM index_day_historical_data WHERE `date`>'2004-12-30' group by `date`")
# myCursor.execute("SELECT `date`,sum(`total_value`) AS total_value2 FROM index_day_historical_data WHERE `date`='2015-01-05' group by `date`")
resultStockList=myCursor.fetchall()
for stocklistkey in range(len(resultStockList)):
	gdpListKey='gdp'+str(resultStockList[stocklistkey][0].year-1)
	dayStockTotal=int(resultStockList[stocklistkey][1])
	# print type(dayStockTotal)
	# print type(gdpList[gdpListKey]*100000000)
	# print dayStockTotal/(gdpList[gdpListKey]*100000000)
	# print '-------'
	GDPratios=dayStockTotal/(gdpList[gdpListKey]*100000000)
	valueee=[resultStockList[stocklistkey][0],GDPratios]
	
	print dayStockTotal,gdpList[gdpListKey]
	print valueee
	
	result=myCursor.execute("INSERT INTO `stock_gdp_ratios`(`date`,`ratios`) VALUES (%s,%s)",valueee)
	# print '-----------------------'+result
