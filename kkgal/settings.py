LOG_LEVEL="WARNING"
USER_AGENT="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"


BOT_NAME = 'kkgal'

SPIDER_MODULES = ['kkgal.spiders']
NEWSPIDER_MODULE = 'kkgal.spiders'

ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
   'kkgal.middlewares.SeleniumMiddleware': 543,
}

MYSQL = {
   'host': '127.0.0.1',
   'port': 3306,
   'db': 'xana',
   'user': 'root',
   'password': '',
   'use_unicode': True,
   'charset': 'utf8',
}