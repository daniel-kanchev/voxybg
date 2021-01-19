import scrapy


class VoxySpider(scrapy.Spider):
    name = 'voxy'
    allowed_domains = ['voxybg.com']
    start_urls = ['http://voxybg.com/']

    def parse(self, response):
        pass
