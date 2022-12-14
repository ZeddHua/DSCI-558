from asyncio.windows_events import NULL
import scrapy
import re
from ..items import ImdbDirectorItem

with open('./Zhenmin_Hua_hw01_movie.jsonlines') as f:
    lst = []
    for i in f.readlines():
        lst.append(eval(i.rstrip('\n')))
hrefs_lst = [i['directors_url'] for i in lst]
hrefs = [i for j in hrefs_lst for i in j]
hrefs = list(set(hrefs))
print(len(hrefs))

class DirectorInfoSpider(scrapy.Spider):
    name = 'directorInfo_spider'
    allowed_domains = ['www.imdb.com']
    start_urls = hrefs

    def parse(self, response):      
        imdb_item = ImdbDirectorItem()

        if response.xpath('//*[@id="name-overview-widget-layout"]/tbody/tr[1]/td/h1/span/text()').extract():
            imdb_item['name'] = response.xpath('//*[@id="name-overview-widget-layout"]/tbody/tr[1]/td/h1/span/text()').extract_first()
        else:                                    
            imdb_item['name'] = response.xpath('//*[@id="overview-top"]/div[1]/div/h1/span/text()').extract_first()
        
        try:
            if response.xpath('//*[@id="name-born-info"]/time/a[1]/text()').extract(): 
                birth_date = response.xpath('//*[@id="name-born-info"]/time/a[1]/text()').extract_first()
                birth_year = response.xpath('//*[@id="name-born-info"]/time/a[2]/text()').extract_first()
                imdb_item['birthDate'] = birth_date + ', ' + birth_year
            else:
                imdb_item['birthDate'] = 'null'
        except:
            imdb_item['birthDate'] = 'null'
        
        try:
            if response.xpath('//*[@id="name-death-info"]/time/a[1]/text()').extract(): 
                death_date = response.xpath('//*[@id="name-death-info"]/time/a[1]/text()').extract_first()
                death_year = response.xpath('//*[@id="name-death-info"]/time/a[2]/text()').extract_first()
                imdb_item['deathDate'] = death_date + ', ' + death_year
            else:
                imdb_item['deathDate'] = 'null'
        except:
            imdb_item['deathDate'] = 'null'

        try:
            if response.xpath('//*[@id="name-bio-text"]/div/div/span/a/text()').extract(): 
                bio_link = 'https://www.imdb.com' + response.xpath('//*[@id="name-bio-text"]/div/div/span/a/@href').extract_first()
                yield scrapy.Request(bio_link, callback=self.parse_bio, meta={'item': imdb_item})
            else:
                imdb_item['biography'] = 'null'
                yield imdb_item
        except:
            imdb_item['biography'] = 'null'
            yield imdb_item

    def parse_bio(self, response):
        imdb_item = response.meta['item']
        try:
            text = response.xpath('//*[@id="bio_content"]/div[2]/p[1]//text()').extract()
            imdb_item['biography'] = ' '.join(text).strip('\n').strip(' ').strip('\n')
            yield imdb_item
        except:
            imdb_item['biography'] = 'null'
            yield imdb_item