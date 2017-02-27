#!/bin/bash                                                                                                                                           
# 0 17 * * * sh /vagrant/code/ChinaStockCrawler/runEveryday.sh
# sed -i 's/\r//' script.sh

cd /vagrant/code/ChinaStockCrawler/MainCrawler && scrapy crawl stockExchangeTask

# # PATH=$PATH:/usr/local/bin
# # export PATH