# -*- coding: utf-8 -*-
# @Time  : 2022/7/27 22:29
# @Author: Lihaocheng
# @File  : company_spider.py

import scrapy
from scrapy.http import Request
from scrapy import Spider
from scrapy.shell import inspect_response
import re
import json
from items import CompanysItem


class CompanySpider(Spider):
    name = 'Company'

    def start_requests(self):
        header = {
            'referer': "http://www.sse.com.cn/assortment/stock/areatrade/area/detail.shtml",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71",
        }
        url = 'http://www.sse.com.cn/js/common/ssesuggestdata.js?v=202272723'
        yield Request(url, callback=self.parse, headers=header)

    def parse(self, response):
        headers = {
            'Referer': 'http://stockpage.10jqka.com.cn/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71',
            'cookie': "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1658930264; __utma=156575163.744850703.1658930282.1658930282.1658930282.1; __utmc=156575163; __utmz=156575163.1658930282.1.1.utmcsr=stockpage.10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmb=156575163.1.10.1658930282; log=; historystock=601368; spversion=20130314; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1658930794; reviewJump=nojump; searchGuide=sg; usersurvey=1; v=A2SOSlfh2ja5PS76aJGbcBgDNWlT_YhnSiEcq36F8C_yKQpXpg1Y95ox7DnN"
        }
        # inspect_response(response, self)
        code_list = re.findall(r'val:"(\d+)"',response.text)
        for code in code_list:
            item = CompanysItem()
            item['code'] = code
            yield Request(f"http://basic.10jqka.com.cn/{code}/company.html", self.parse_further, meta={'item1': item},
                          headers=headers)

    def parse_further(self, response):
        # inspect_response(response,self)
        code = response.meta['item1']['code']
        comp = response.xpath("//tr[@class='video-btn-box-tr']/td[2]/span/text()").extract()[0]
        name_list = response.xpath("//td[@class='tc name']")
        for name in name_list:
            item = CompanysItem()
            item['company'] = comp
            item['code'] = code
            item['name'] = name.xpath("./a/text()").extract()[0]
            item['job'] = name.xpath("./div/table/thead/tr[1]/td[@class='jobs']/text()").extract()[0]
            intro_strs = name.xpath("./div/table/thead/tr[2]/td[@class='intro']/text()").extract()[0]
            item['age'] = re.findall(r'-?[1-9]\d*岁', intro_strs)[0]
            item['gender'] = re.findall(r"^.",intro_strs)[0]
            yield item


        # dic = json.loads(response.text)
        # list = dic['data']['list']
        # for i in list:
        #     item = BilibiliItem()
        #     item['title'] = i['title']
        #     item['author'] = i['owner']['name']
        #     item['coin'] = i['stat']['coin']
        #     item['bvid'] = i['bvid']
        #     item['dynamic'] = i['dynamic'].replace('\n', '')
        #     item['url'] = self.base_url + '/video/' + item['bvid']
        #     yield Request(item['url'] + '?vd_source=65aa9381fce2b80aa78e4f2be0b3e7c6', callback=self.parse_file,
        #                   meta={'item': item}, headers=headers)
