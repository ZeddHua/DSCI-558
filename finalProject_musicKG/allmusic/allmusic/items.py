# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AllmusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# class starting_Item(scrapy.Item):
#     genre = scrapy.Field() 
#     url = scrapy.Field() 

class genre_Item(scrapy.Item):
    title = scrapy.Field() 
    discription = scrapy.Field() 
    url = scrapy.Field()
    sub_genre = scrapy.Field()
    sub_genre_url = scrapy.Field()

class song_Item(scrapy.Item):
    title = scrapy.Field() 
    url = scrapy.Field()
    performer = scrapy.Field() 
    performer_url = scrapy.Field()
    composer = scrapy.Field()
    composer_url = scrapy.Field()
    release_year = scrapy.Field()
    genres = scrapy.Field()
    styles = scrapy.Field()
    moods = scrapy.Field()
    themes = scrapy.Field()
    in_album = scrapy.Field()
    album_url = scrapy.Field()
    time = scrapy.Field()

class artist_Item(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    biography = scrapy.Field()
    active_years = scrapy.Field()
    born_in = scrapy.Field()
    genres = scrapy.Field()
    styles =  scrapy.Field()
    aliases =  scrapy.Field()
    group_members = scrapy.Field()
    group_members_url = scrapy.Field()