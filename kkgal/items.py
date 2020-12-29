
import scrapy

class KkgalItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    sellDate = scrapy.Field()
    pic = scrapy.Field()
    des1 = scrapy.Field()
    des2 = scrapy.Field()
    tags = scrapy.Field()