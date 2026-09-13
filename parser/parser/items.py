import scrapy


class CurrencyRateItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    nominal = scrapy.Field()
    value = scrapy.Field()
    date = scrapy.Field()
