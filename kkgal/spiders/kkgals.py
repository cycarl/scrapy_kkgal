import re

import MySQLdb
import scrapy

from kkgal.items import KkgalItem

from kkgal.settings import MYSQL


class KkgalsSpider(scrapy.Spider):
    name = 'kkgals'
    # allowed_domains = ['www.kkgal.com']
    start_urls = ['https://www.kkgal.com/']

    def __init__(self):
        self.start_urls = input().split()
        self.con = MySQLdb.connect(**MYSQL)
        self.cur = self.con.cursor()
        self.sql = 'insert into games(id, title, pic, des1, des2, sellDate, tags) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")';
        self.sql1 = 'insert into pics values (NULL, "%s", "%s")';
        self.reg = r'([^/]+?)\.html$'


    def parse(self, response, **kwargs):
        yield scrapy.Request(url=response.url, callback=self.parse_page)

        # yield scrapy.Request(url=response.url, callback=self.parse_detail)

        pass


    def parse_page(self, response):
        r = re.search(r'page/(\d+)/?$', response.url)
        if r==None: page = 1
        else: page = r.group(1)

        p = int(page)
        if p>91: return



        hrefs = response.css('.mybody3>.ih-item>a::attr(href)').extract()
        for href in hrefs:
            if 'gengxinrizhi' in href:
                continue
            yield scrapy.Request(url=href, callback=self.parse_detail)

        # print("==============================第%s页=========================================" % p)

        next_page = 'https://www.kkgal.com/page/%s/'%(p+1)
        yield scrapy.Request(url=next_page, callback=self.parse_page)

    def parse_detail(self, response):

        item = KkgalItem()

        main = response.css("article[class='article container well a-rotateinLT mybody3']")
        item['id'] = re.search(self.reg, response.url).group(1)
        item['title'] = main.css('h1>a::text').extract_first()

        pics = main.css('.centent-article>.dAnim>a::attr(href)').extract()
        item['pic'] = main.css('.dAnim>a::attr(href)').extract()[1]
        des = main.css('.alert-success')
        item['des1'] = ''
        item['des2'] = ''

        item['sellDate'] = main.css('.label-zan::text').extract_first()
        item['tags'] = ' '.join(main.css(".article-tags>a::text").extract())
        #

        if len(des)>0:
            item['des1'] =  self.parse_deal('<br>'.join(des[0].css("::text").extract()))
        if len(des)>1:
            item['des2'] = self.parse_deal('<br>'.join(des[-1].css("::text").extract()))
        # print(item)
        tp = tuple(item.values())
        try:
            self.cur.execute(self.sql%tp)
            for pic in pics:
                self.cur.execute(self.sql1%(item['id'], pic))
            self.con.commit()
        except:
            print('======================【%s】发生数据库异常==========================='%item['title'])


    def parse_deal(self, des):
        return re.sub(r'\"+', r"'", des)