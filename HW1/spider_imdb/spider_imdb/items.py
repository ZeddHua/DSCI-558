# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderImdbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    rank = scrapy.Field()
    url = scrapy.Field()

class ImdbMovieItem(scrapy.Item):
    title = scrapy.Field()
    directors = scrapy.Field()
    directors_url = scrapy.Field()
    plot = scrapy.Field()
    actors = scrapy.Field()

class ImdbDirectorItem(scrapy.Item):
    name = scrapy.Field()
    birthDate = scrapy.Field()
    deathDate = scrapy.Field()
    biography = scrapy.Field()

