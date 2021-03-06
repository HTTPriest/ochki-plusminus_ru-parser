# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OchkiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    model = scrapy.Field()
    manufacturer = scrapy.Field()
    is_available = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    #reviews = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass
