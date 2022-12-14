import scrapy
import re
from ..items import SpiderImdbItem

class ImdbSpiderSpider(scrapy.Spider):
    name = 'imdb_spider'
    allowed_domains = ['www.imdb.com']
    start_urls = ['http://www.imdb.com/chart/top']

    def parse(self, response):
        items = []
        
        for i in range(1,251):
            imdb_item = SpiderImdbItem()

            imdb_item['title'] = response.xpath(f'//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[{i}]/td[2]/a/text()').extract_first()
            imdb_item['year'] = response.xpath(f'//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[{i}]/td[2]/span/text()').extract_first().lstrip('(').rstrip(')')
            imdb_item['rank'] = re.findall(r"\d+", response.xpath(f'//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[{i}]/td[2]/text()').extract_first())[0]
            imdb_item['url'] = 'https://www.imdb.com' + response.xpath(f'//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[{i}]/td[2]/a/@href').extract_first()

            # 不进行 yield 无法进入 pipelines 里面,将获取的数据交给pipelines
            #yield imdb_item
            items.append(imdb_item)

        #yield scrapy.Request('http://www.imdb.com/chart/top', callback=self.parse)
        return items
