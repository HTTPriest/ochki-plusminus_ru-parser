# -*- coding: utf-8 -*-
import scrapy
import base64
from scrapy_splash import SplashRequest, SplashFormRequest
from time import time
from ochki.items import OchkiItem
from urllib.parse import urljoin, urlparse
from functools import reduce
from unicodedata import normalize


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['ochki-plusminus.ru']


    def screenshot(self, response):
        imgdata = base64.b64decode(response.data['png'])
        filename = 'save/screenshot%s.png' % time()
        with open(filename, 'wb') as f:
            f.write(imgdata)

    lua_script = '''
            function main(splash)
                if splash.args.cookies then
                    splash:init_cookies(splash.args.cookies)
                end
                assert(splash:go{
                    splash.args.url,
                    headers=splash.args.headers,
                    http_method=splash.args.http_method,
                    body=splash.args.body,
                    formdata=splash.args.formdata
                })
                assert(splash:wait(0.5))

                local entries = splash:history()
                local last_response = entries[#entries].response

                return {
                    url = splash:url(),
                    headers = last_response.headers,
                    http_status = last_response.status,
                    cookies = splash:get_cookies(),
                    html = splash:html(),
                    png = splash:png(),
                }
            end
            '''

    def start_requests(self):
        yield SplashRequest('http://ochki-plusminus.ru/index.php?route=account/login',
                            callback=self.login,
                            endpoint='execute',
                            method='POST',
                            args={'wait': 2,
                                  'lua_source': self.lua_script,
                                  'formdata': {
                                      'email': 'htpriestx@gmail.com',
                                      'password': 'all5885'
                                              },
                                  }
                            )

    def login(self, response):
        logout = response.xpath('//a[@href=contains(., "logout")]')
        self.log('Page loaded')
        #self.log(logout)
        self.screenshot(response)

        yield SplashRequest('http://ochki-plusminus.ru/',
                            endpoint='execute',
                            method='GET',
                            args={'wait': 2,
                                  'lua_source': self.lua_script,
                                  })


    def parse(self, response):
        self.screenshot(response)
        registration = response.xpath('//a[@target="регистрации"]')
        if registration:
            self.log('LOGIN HAS FAILED')
        else:
            self.log('LOGIN SUCCESSFUL')
            menu = response.xpath('//ul[@id="menu-vertical-list"]')

            #   parsing depth limit
            for option in menu.xpath('./li[not(contains(@class,"hidden-md hidden-lg"))]')[:2]:
                link = option.xpath('./a/@href').extract()[0]

                self.log(link)
                yield SplashRequest(urljoin('http://ochki-plusminus.ru', link),
                                    callback=self.parse_category,
                                    endpoint='execute',
                                    method='GET',
                                    args={
                                        'wait': 1,
                                        'lua_source': self.lua_script,
                                    })

    def parse_category(self, response):
        #   yield items
        links = response.xpath('//h4/a/@href')
        for link in links:
            link = link.extract()
            self.log('Link from category : %s' % link)
            yield SplashRequest(link,
                                callback=self.parse_item,
                                endpoint='execute',
                                method='GET',
                                args={
                                    'wait': 2,
                                    'lua_source': self.lua_script,
                                })
        #   pagination
        next_url = response.xpath('//ul[@class="pagination"]/li[@class="active"]/following-sibling::li/a/@href').extract()[0]
        self.log('Next sibling::: ')
        self.log(next_url)
        yield SplashRequest(next_url,
                            callback=self.parse_category,
                            endpoint='execute',
                            method='GET',
                            args={
                                'wait': 2,
                                'lua_source': self.lua_script,
                            })



    def parse_item(self, response):

        image = response.xpath('//a[@class="thumbnail"]/@href')
        prod = response.xpath('//div[@id="product"]')
        price = './/h2span[@class=contains(., "autocalc-product-price") or contains(., "autocalc-product-special")]/text()'
        description = response.xpath('string(//div[@id="tab-description"])').extract()
        desc = reduce(lambda x, y: x + y, description)

        product = OchkiItem()
        product['url'] = response.url
        product['name'] = response.xpath('//h1/text()').extract()
        product['model'] = prod.xpath('.//span[text()[contains(., "Модель")]]/text()').extract()
        product['manufacturer'] = response.xpath('//*[text()[contains(., "Производитель")]]/a/text()').extract()
        product['is_available'] = response.xpath('//li[text()[contains(., "Наличие")]]/span/text()').extract()
        product['price'] = [i.split(' ')[0] for i in response.xpath('//i[@class="fa fa-rub"]/parent::span/text()').extract()]
        product['description'] = desc.replace(u'\xa0', ' ').replace(u'\n', '').replace('  ', ' ')
        #product['reviews'] =
        product['category'] = urlparse(response.url).path.split(sep='/')[1]
        #   send image url to pipeline
        product['image_urls'] = response.xpath('//a[@class="thumbnail"]/@href').extract()
        self.log(product)
        yield product
        pass


