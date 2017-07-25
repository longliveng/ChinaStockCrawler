## 开发环境

python 2.7  
scrapy 1.3  
pip install MySQL-python --trusted-host mirrors.aliyun.com 
  

## 数据来源
用同花顺导出了20多年的数据，通过csv文件导入了mysql数据库. 所以除了total_value 和 backup 两列数据是用这个爬虫搞定的，index_day_historical_data表里的其他数据都是同花顺里导出的。。

urlShanghai = 'http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate=2017-01-26&prodType=gp&_=1485967505892'  
urlShenzhen = 'http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.4397416552090172'

## command

scrapy crawl stockExchange -a market=shanghai  
scrapy crawl stockExchange -a market=shenzhen  

scrapy crawl stockExchangeTask  

##about doc
一些数据对照，以后可以拿到buckup里的数据。。

## tips

https://github.com/scrapy/scrapy/issues/2473
pip install Twisted==16.4.1
scrapy 1.4下的 Twisted17 有问题