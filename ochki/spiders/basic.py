# -*- coding: utf-8 -*-
import scrapy
import base64
from scrapy_splash import SplashRequest, SplashFormRequest
from time import time


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['ochki-plusminus.ru']


    def screenshot(self, response):
        imgdata = base64.b64decode(response.data['png'])
        filename = 'screenshot%s.png' % time()
        with open(filename, 'wb') as f:
            f.write(imgdata)


    def start_requests(self):
        body = '''-----------------------------5520711821930979191957072406
Content-Disposition: form-data; name="email"

htpriestx@gmail.com
-----------------------------5520711821930979191957072406
Content-Disposition: form-data; name="password"

all5885
-----------------------------5520711821930979191957072406--

        '''
        yield SplashFormRequest('http://ochki-plusminus.ru/index.php?route=account/login',
                            callback=self.login,
                            endpoint='render.json',
                            args={'wait': 2,
                                  'html': 1,
                                  'png': 1},
                            formdata={'email': 'htpriestx@gmail.com',
                                      'password': 'all5885'}
                            )


    def login(self, response):
        logout = response.xpath('//a[@href=contains(., "logout")]')
        self.log('Page loaded')
        self.log(logout)
        self.screenshot(response)

        yield SplashRequest('http://ochki-plusminus.ru/',
                                endpoint='render.json',
                                args={'wait': 2,
                                      'html': 1,
                                      'png': 1})


    def parse(self, response):
        self.screenshot(response)
        registration = response.xpath('//a[@target="регистрации"]')
        if registration:
            self.log('LOGIN HAS FAILED')




