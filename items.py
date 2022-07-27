# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanysItem(scrapy.Item):
    # define the fields for your item here like:
    company = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    job  = scrapy.Field()
    gender = scrapy.Field()
    age = scrapy.Field()

    pass
