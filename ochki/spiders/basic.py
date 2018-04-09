# -*- coding: utf-8 -*-
import scrapy


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['ochki-plusminus.ru']
    start_urls = ['http://ochki-plusminus.ru/']

    def parse(self, response):
        pass
