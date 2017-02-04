# -*- coding: utf-8 -*-
import MySQLdb
import sys
import MySQLdb
import json

dbpool=MySQLdb.connect(
	host='127.0.0.1',
	db = 'stock_data',
	user = 'root',
	passwd = 'cyhcyh',
	port=3306,
	charset = 'utf8',
)
myCursor=dbpool.cursor()

myCursor.execute('SELECT backup,id FROM index_day_historical_data WHERE `type` = 000001')
resultStockList=myCursor.fetchall()

# print resultStockList
# exit()
print('-----------shanghai---------------')
for stocklistkey in range(len(resultStockList)):
	resDict=json.loads(resultStockList[stocklistkey][0])
	if resDict['result'][2]['marketValue1']=='':
		resDict['result'][2]['marketValue1']=0
	else:
		# print resDict['result'][2]['marketValue1']
		resDict['result'][2]['marketValue1']=float(resDict['result'][2]['marketValue1'])
		resDict['result'][2]['marketValue1']=resDict['result'][2]['marketValue1']*100000000
		# print resDict['result'][2]['marketValue1']
		# exit()

	updateSql="UPDATE `index_day_historical_data` SET `total_value` = "+str(resDict['result'][2]['marketValue1'])+" WHERE `id`='"+str(resultStockList[stocklistkey][1])+"'";
	# # print updateSql
	# # exit()
	myCursor.execute(updateSql)