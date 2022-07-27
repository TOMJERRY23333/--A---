# -*- coding: utf-8 -*-
# @Time  : 2022/7/27 23:26
# @Author: Lihaocheng
# @File  : run.py

#!/usr/bin/env python
# encoding: utf-8

import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.company_spider import CompanySpider



if __name__ == '__main__':
    mode = sys.argv[1]
    os.environ['SCRAPY_SETTINGS_MODULE'] = f'settings'
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    mode_to_spider = {
        'comp': CompanySpider
    }
    process.crawl(mode_to_spider[mode])
    # the script will block here until the crawling is finished
    process.start()
