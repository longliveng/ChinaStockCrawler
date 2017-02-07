#!/bin/bash
# 0 17 * * * /vagrant/code/ChinaStockCrawler/MainCrawler/runEveryday.sh

cd /vagrant/code/ChinaStockCrawler/MainCrawler
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl stockExchangeTask