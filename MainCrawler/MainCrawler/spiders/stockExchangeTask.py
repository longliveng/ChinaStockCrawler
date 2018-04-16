# -*- coding: utf-8 -*-
from scrapy.mail import MailSender
import scrapy
import time
import datetime
import pymysql.cursors
import json

# from MainCrawler.items import *


class StockexchangetaskSpider(scrapy.Spider):

    name = "stockExchangeTask"
    updateDayNum = 4
    # allowed_domains = ["sfds.com"]

    def __init__(self, *args, **kwargs):
        super(StockexchangetaskSpider, self).__init__(*args, **kwargs)
        if self.updateDayNum <= 1:
            exit()

        self.aboutMysql()

    def aboutMysql(self):
        # Connect to the database
        self.dbCon = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='cyhcyh',
            db='stock_data',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)

        self.myCursor = self.dbCon.cursor()

    def start_requests(self):
        # urlShanghai = 'http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate=2017-01-26&prodType=gp&_=1485967505892'
        # urlShenzhen = 'http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.4397416552090172'

        self.aboutMysql()
        self.now = datetime.datetime.now()
        # 下面这条取消注释，相当于setting开始日期
        # self.now=datetime.datetime.strptime('2017-05-26 00:53:28',"%Y-%m-%d %H:%M:%S")
        self.todayDate = str(self.now.strftime('%Y-%m-%d'))

        # print type(self.settings['MY_EMAIL'])

        resultUrl = []

        resultUrl = self.generateShanghai()
        resultUrl.extend(self.generateShenzhen())

        return resultUrl

    # 数据源: http://www.sse.com.cn/market/stockdata/overview/day/?&lan=cn&lan=cn&lan=cn
    def generateShanghai(self):
        shanghaiHeaders = {
            "Host":
            "query.sse.com.cn",
            "Referer":
            "http://www.sse.com.cn/market/stockdata/overview/day/?&lan=cn&lan=cn&lan=cn",
            "Connection":
            "keep-alive"
        }
        resultUrl = []

        print('-----------shanghai---------------')
        for dayKey in range(self.updateDayNum):
            gapDay = int(-dayKey)
            whereDate = self.now + datetime.timedelta(days=gapDay)
            whereDate = str(whereDate.strftime('%Y-%m-%d'))

            self.myCursor.execute(
                'SELECT `date`,`total_value` FROM index_day_historical_data WHERE `type` = 000001 and `date`="'
                + whereDate + '"')

            resultStock = self.myCursor.fetchone()

            if resultStock is None:
                # 没数据
                urlShanghai = 'http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate=' + \
                    whereDate + '&prodType=gp&_=1485967505892'

                responsesss = scrapy.Request(
                    url=urlShanghai,
                    callback=self.indexDayParseShanghai,
                    headers=shanghaiHeaders)
                responsesss.meta['isFirst'] = True
            else:
                # 有数据
                # print('ffffffffffffffffff')
                # print(whereDate)
                # print(resultStock)
                # exit()
                urlShanghai = 'http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate=' + str(
                    resultStock['date']) + '&prodType=gp&_=1485967505892'

                responsesss = scrapy.Request(
                    url=urlShanghai,
                    callback=self.indexDayParseShanghai,
                    headers=shanghaiHeaders)
                responsesss.meta['isFirst'] = False

            resultUrl.append(responsesss)

        return resultUrl

    # 数据源: http://www.szse.cn/main/marketdata/tjsj/jyjg/
    def generateShenzhen(self):
        shenzhenFormdata = {
            "ACTIONID": "7",
            "AJAX": "AJAX-TRUE",
            "CATALOGID": "1803",
            "TABKEY": "tab1",
            "REPORT_ACTION": "search",
            "txtQueryDate": "",
        }
        resultUrl = []

        print('-----------shenzhen---------------')
        for dayKey in range(self.updateDayNum):
            gapDay = int(-dayKey)
            whereDate = self.now + datetime.timedelta(days=gapDay)
            whereDate = str(whereDate.strftime('%Y-%m-%d'))
            # whereDate='2015-06-05'

            self.myCursor.execute(
                'SELECT * FROM index_day_historical_data WHERE `type` = 399001 and `date`="'
                + whereDate + '"')
            resultStock = self.myCursor.fetchone()

            urlShenzhen = 'http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.5798621223025'
            if resultStock is None:
                # 没数据
                shenzhenFormdata['txtQueryDate'] = whereDate
                responsesss = scrapy.FormRequest(
                    url=urlShenzhen,
                    callback=self.indexDayParseShenzhen,
                    formdata=shenzhenFormdata)
                responsesss.meta['isFirst'] = True
            else:
                # 有数据
                shenzhenFormdata['txtQueryDate'] = whereDate
                responsesss = scrapy.FormRequest(
                    url=urlShenzhen,
                    callback=self.indexDayParseShenzhen,
                    formdata=shenzhenFormdata)
                responsesss.meta['isFirst'] = False

            resultUrl.append(responsesss)

        return resultUrl

    def indexDayParseShanghai(self, response):
        print('-----------------indexDayParseShanghai------------------------')

        resJson = response.text[19:-1]
        resDict = json.loads(resJson)

        print('~~~~~~~~~~today is ' + str(resDict['searchDate']))

        if resDict['result'][2]['marketValue1'] == '':
            return
        else:
            resDict['result'][2]['marketValue1'] = float(
                resDict['result'][2]['marketValue1'])
            resDict['result'][2]['marketValue1'] = resDict['result'][2][
                'marketValue1'] * 100000000

        currentStamp = str(int(time.time()))

        if response.meta['isFirst']:
            blablaSql = "INSERT INTO `index_day_historical_data`(`total_value`,`backup`,`type`,`date`,`update_time`)VALUES(" + str(
                resDict['result'][2]
                ['marketValue1']) + ",'" + str(resJson) + "','000001','" + str(
                    resDict['searchDate']) + "','" + currentStamp + "');"
        else:
            blablaSql = "UPDATE `index_day_historical_data` SET `total_value` = " + str(
                resDict['result'][2]['marketValue1']
            ) + ",`backup` = '" + resJson + "',`update_time` = " + currentStamp + " WHERE `type` = 000001 and `date`='" + str(
                resDict['searchDate']) + "';"
        # print blablaSql
        # exit()
        self.myCursor.execute(blablaSql)
        self.dbCon.commit()

    def indexDayParseShenzhen(self, response):
        print(
            '-----------------indexDayParseShenzhen--!!------------------------'
        )
        # currDate = response.xpath('//input[@id="1804_gid_tab1_con_txtDate"]/@value').extract()
        # currDate = str(currDate[0])
        # resultMarketValue=response.xpath('//table[@id="REPORTID_tab1"]/tr[2]/td[6]/text()').extract()

        currDate = response.xpath(
            '//input[@id="1803_gid_tab1_con_txtQueryDate"]/@value').extract()
        currDate = str(currDate[0])
        resultMarketValue = response.xpath(
            u"//td[.='股票总市值（元）']/../td[2]/text()").extract()

        print('~~~~~~~~~~today is ' + currDate)

        if resultMarketValue == []:
            return
        else:
            resultMarketValue = resultMarketValue[0]
            resultMarketValue = resultMarketValue.replace(',', '')

        # 过滤 html,pure SB
        responseText = response.text.replace('\'', '\"')

        currentStamp = str(int(time.time()))

        if response.meta['isFirst']:
            blablaSql = "INSERT INTO `index_day_historical_data`(`total_value`,`backup`,`type`,`date`,`update_time`)VALUES(" + str(
                resultMarketValue) + ",'" + str(
                    responseText) + "','399001','" + str(
                        currDate) + "','" + currentStamp + "');"
        else:
            blablaSql = "UPDATE `index_day_historical_data` SET `total_value` = " + str(
                resultMarketValue
            ) + ",`backup` = '" + responseText + "',`update_time` = " + currentStamp + " WHERE `type` = 399001 and `date`='" + str(
                currDate) + "';"
        # print blablaSql
        # exit()
        self.myCursor.execute(blablaSql)
        self.dbCon.commit()

    def closed(self, reason):
        # GDP绝对值 单位(亿元)

        gdpList = {
            'gdp2017': 827122,
            'gdp2016': 744127,
            'gdp2015': 676708,
            'gdp2014': 635910,
            'gdp2013': 588018.76,
            'gdp2012': 534123.04,
            'gdp2011': 473104.05,
            'gdp2010': 401512.8,
            'gdp2009': 340902.81,
            'gdp2008': 314045.4,
            'gdp2007': 265810.3,
            'gdp2006': 216314.4,
            'gdp2005': 184937.4,
            'gdp2004': 159878.3,
            'gdp2003': 135822.8,
            'gdp2002': 120332.7,
            'gdp2001': 109655.2,
            'gdp2000': 99214.6,
            'gdp1999': 89677.1,
            'gdp1998': 84402.3,
            'gdp1997': 78973,
            'gdp1996': 71176.6,
            'gdp1995': 60793.7,
            'gdp1994': 48197.9,
            'gdp1993': 35333.9,
            'gdp1992': 26923.5,
            'gdp1991': 21781.5
        }

        # 最近几天的数据
        self.myCursor.execute(
            "SELECT `date`,sum(`total_value`) AS total_value2 FROM index_day_historical_data group by `date` order by date desc limit "
            + str(self.updateDayNum))
        dayHistoricalDataList = self.myCursor.fetchall()
        # print(dayHistoricalDataList)
        # print(self.updateDayNum)
        # exit()
        for dayHistoricalDataListKey in range(len(dayHistoricalDataList)):
            currentDay = dayHistoricalDataList[dayHistoricalDataListKey]['date']
            currentDayStr = str(currentDay.strftime('%Y-%m-%d'))

            # get GDP
            gdpListKey = 'gdp' + str(currentDay.year - 1)
            dayStockTotal = int(
                dayHistoricalDataList[dayHistoricalDataListKey]['total_value2'])

            GDPratios = dayStockTotal / (gdpList[gdpListKey] * 100000000)
            valueee = [currentDayStr, GDPratios]

            # update data
            self.myCursor.execute(
                "SELECT * FROM stock_gdp_ratios WHERE `date`='" + currentDayStr
                + "'")
            resultStockRecord = self.myCursor.fetchone()

            if resultStockRecord is None:
                self.myCursor.execute(
                    "INSERT INTO `stock_gdp_ratios`(`date`,`ratios`) VALUES (%s,%s)",
                    valueee)
            else:
                updateValue = [valueee[1], valueee[0]]
                self.myCursor.execute(
                    "UPDATE `stock_gdp_ratios` SET  `ratios` = %s WHERE `date`=%s;",
                    updateValue)

            self.dbCon.commit()

            if dayHistoricalDataListKey == 0 and resultStockRecord is None:
                # 发邮件
                mailer = MailSender.from_settings(self.settings)
                title = "证券化率：" + str(GDPratios)
                body = "证券化率：" + str(GDPratios) + "<br/>" + "总市值：" + str(
                    dayStockTotal) + "元  <br/>当前日期: " + currentDayStr
                mailer.send(
                    to=self.settings['SEND_TO_EMAIL'],
                    subject=title,
                    body=body,
                    mimetype="text/html")
