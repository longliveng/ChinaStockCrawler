#!/bin/sh                                                                                                                                           
# 0 19 * * * cd /var/www/html/ChinaStockCrawler/MainCrawler/MainCrawler/spiders && /usr/local/bin/scrapy runspider stockExchangeTask.py
# sed -i 's/\r//' script.sh
# cd /vagrant/code/ChinaStockCrawler/MainCrawler && python3 -m scrapy crawl stockExchangeTask

cd /vagrant/code/ChinaStockCrawler/MainCrawler &&
python2 -m scrapy crawl stockExchangeTask

# # PATH=$PATH:/usr/local/bin
# # export PATH