#!/bin/sh                                                                                                                                           
# 0 19 * * * cd /vagrant/code/ChinaStockCrawler/MainCrawler && /usr/local/bin/scrapy crawl stockExchangeTask
# sed -i 's/\r//' script.sh

cd /vagrant/code/ChinaStockCrawler/MainCrawler
/usr/local/bin/scrapy crawl stockExchangeTask

# # PATH=$PATH:/usr/local/bin
# # export PATH