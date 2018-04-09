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




