# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ModelItem(scrapy.Item):
    name = scrapy.Field()
    phone = scrapy.Field()
    photoLinks = scrapy.Field()
