import scrapy
import re
from ..items import ImdbMovieItem

with open('./Zhenmin_Hua_hw01_movielist.jsonlines') as f:
    lst = []
    for i in f.readlines():
        lst.append(eval(i.rstrip('\n')))
hrefs = [i['url'] for i in lst]

class MovieInfoSpider(scrapy.Spider):
    name = 'movieInfo_spider'
    allowed_domains = ['www.imdb.com']
    start_urls = hrefs

    def parse(self, response):
        imdb_item = ImdbMovieItem()

        imdb_item['title'] = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/text()').extract_first()
        imdb_item['directors'] = response.xpath('//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[1]/div/ul/li/a/text()').extract()
        imdb_item['directors_url'] = ['https://www.imdb.com' + i for i in response.xpath('//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[4]/ul/li[1]/div/ul/li/a/@href').extract()]
        imdb_item['plot'] = response.xpath('//span[contains(@data-testid, "plot-xl")]/text()').extract_first()                     
        imdb_item['actors'] =response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/div/ul/li/a/text()').extract()
        
        return imdb_item