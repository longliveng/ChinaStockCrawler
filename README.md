## 开发环境

python 2.7  
scrapy 1.3  
pip install MySQL-python --trusted-host mirrors.aliyun.com 
  

## 数据来源

urlShanghai = 'http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback63703&searchDate=2017-01-26&prodType=gp&_=1485967505892'  
urlShenzhen = 'http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.4397416552090172'

## command

scrapy crawl stockExchange -a market=shanghai 