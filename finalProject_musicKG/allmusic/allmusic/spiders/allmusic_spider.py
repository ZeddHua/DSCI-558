import scrapy
import json
import re

from allmusic.items import *

def clean(list):
    for item in list:
        if '\n' in list:
            list.remove(item)
    return list


class allmusic_Spider(scrapy.Spider):
    name = "all_music"

    start_urls = ['https://www.allmusic.com/genres']
    allowed_domains = ['allmusic.com']

    def parse(self, response):

        # genre_list = response.xpath('//*[@id="cmn_wrap"]/div/div/div[2]/div[*]/h2/a/text()').extract()
        genre_url_list =  response.xpath('//*[@id="cmn_wrap"]/div/div/div[2]/div[*]/h2/a/@href').extract()
        # for i in range(len(genre_list)):
        #     starting_obj = starting_Item()
        #     starting_obj['genre'] = genre_list[i]
        #     starting_obj['url'] = genre_url_list[i]
        #     yield starting_obj

        for url in genre_url_list:
            if url[0] != 'h':
                url = "https://www.allmusic.com" + url
            yield scrapy.Request(url, callback = self.parse_genre)

        moods_url = 'https://www.allmusic.com/moods'
        yield scrapy.Request(moods_url, callback = self.parse_moods_list)

        themes_url = 'https://www.allmusic.com/themes'
        yield scrapy.Request(themes_url, callback = self.parse_theme_list)

    def parse_moods_list(self, response):
        moods_url_list = response.xpath('//*[@id="all-moods-grid-desktop"]/div[*]/div[*]/a/@href').extract()
        for url in moods_url_list:
            if url[0] != 'h':
                url = "https://www.allmusic.com" + url
            yield scrapy.Request(url + '/songs', callback = self.parse_moods)
            yield scrapy.Request(url + '/albums', callback = self.parse_album_list)        

    def parse_moods(self, response):
        song_url_list = response.xpath('//*[@id="cmn_wrap"]/div/div[2]/section/table/tr[*]/td[1]/a/@href').extract()
        for url in song_url_list:
            if url[0] != 'h':
                url = "https://www.allmusic.com" + url
            yield scrapy.Request(url, callback = self.parse_song)   
            

    def parse_theme_list(self, response):
        theme_url_list = response.xpath('//*[@id="all-themes-grid-desktop"]/div[*]/div[*]/a/@href').extract()
        for url in theme_url_list:
            if url[0] != 'h':
                url = "https://www.allmusic.com" + url
            yield scrapy.Request(url + '/songs', callback = self.parse_themes)
            yield scrapy.Request(url + '/albums', callback = self.parse_album_list)    
    
    def parse_themes(self, response):
        song_url_list = response.xpath('//*[@id="cmn_wrap"]/div/div[2]/section[1]/table/tr[*]/td[1]/a[1]/@href').extract()
        for url in song_url_list:
            if url[0] != 'h':
                url = "https://www.allmusic.com" + url
            yield scrapy.Request(url, callback = self.parse_song)  

    def parse_genre(self, response):
        genre_name = response.xpath('//*[@id="cmn_wrap"]/div/div[2]/header/hgroup/h1["genre-name headline"]/text()').extract()
        if not genre_name:
            genre_name =  response.xpath('//*[@id="cmn_wrap"]/div/div[2]/header/hgroup/h1/a//text()').extract()
            for item in genre_name:
                item = item.strip()
        genre_url = response.url
        genre_discription = response.xpath('//*[@id="cmn_wrap"]/div/div[2]/header/div[2]/p["description"]/text()').extract()
        sub_genre_list =  response.xpath('//*[contains(@id,"col")]/ul/li[*]/ul/li[*]/a/text()').extract()
        sub_genre_url_list =  response.xpath('//*[contains(@id,"col")]/ul/li[*]/ul/li[*]/a/@href').extract()

        # artists_list_url = "allmusic.com" + response.xpath('//*[@id="cmn_wrap"]/div/div[2]/section[1]/h4/a/@href').extract()[0]
        # albums_list_url = "allmusic.com" + response.xpath('//*[@id="cmn_wrap"]/div/div[2]/section[2]/h4/a/@href').extract()[0]
        songs_list_url = response.xpath('//*[@id="cmn_wrap"]/div/div[2]/section[3]/h4/a/@href').extract()
        
        genre_obj = genre_Item()
        genre_obj['title'] = genre_name[-1].strip()
        genre_obj['url'] = genre_url
        if genre_discription:
            genre_obj['discription'] = genre_discription[0].replace('\n', '')
        if sub_genre_list:
            genre_obj['sub_genre'] = sub_genre_list
            for url in sub_genre_url_list:
                url = "allmusic.com" + url
            genre_obj['sub_genre_url'] = sub_genre_url_list

        yield genre_obj

        for url in sub_genre_url_list:
            if url[0] != 'h':
                url = "https://www.allmusic.com" + url
            yield scrapy.Request(url, callback = self.parse_genre)

        # yield scrapy.Request(artists_list_url, callback = self.parse_artist_list)
        # yield scrapy.Request(albums_list_url, callback = self.parse_album_list)
        if songs_list_url:
            songs_list_url = "https://www.allmusic.com" + songs_list_url[0]
            yield scrapy.Request(genre_url, callback = self.parse_song_list)

        # album_list_url =  response.xpath('//*[@id="cmn_wrap"]/div/div[2]/section[1]//@href').extract()
        # for url in album_list_url:
        yield scrapy.Request(response.url + '/albums', callback = self.parse_album_list)
    
    def parse_album_list(self, response):
        album_list_url =  response.xpath('//*[@id="cmn_wrap"]/div/div[2]/section[1]//@href').extract()
        if album_list_url:
            for url in album_list_url:
                if 'album' in url:
                    if url[0] != 'h':
                        url = "https://www.allmusic.com" + url
                    yield scrapy.Request(url, callback = self.parse_album)

    def parse_song_list(self, response):
        song_url_list = response.xpath('//*[@id="cmn_wrap"]/div/div[2]/section[1]/table/tr[*]/td[1]/a/@href').extract()
        if song_url_list:
            for url in song_url_list:
                if url[0] != 'h':
                    url = "https://www.allmusic.com" + url
                    yield scrapy.Request(url, callback = self.parse_song)

        composer_url_list = response.xpath('//*[@id="cmn_wrap"]/div/div[2]/section[1]/table/tr[*]/td[1]/div/a/@href').extract()
        if composer_url_list:
            for url in composer_url_list:
                if url[0] != 'h':
                    url = "https://www.allmusic.com" + url
                    yield scrapy.Request(url, callback = self.parse_artist)

        performer_url_list =  response.xpath('//*[@id="cmn_wrap"]/div/div[2]/section[1]/table/tr[*]/td[2]/a/@href').extract()
        if performer_url_list:
            for url in performer_url_list:
                if url[0] != 'h':
                    url = "https://www.allmusic.com" + url
                    yield scrapy.Request(url, callback = self.parse_artist)

        # for url in song_url_list:
        #     yield scrapy.Request(url, callback = self.parse_song)

        # for url in composer_url_list:
        #     yield scrapy.Request(url, callback = self.parse_artist)

        # for url in performer_url_list:
        #     yield scrapy.Request(url, callback = self.parse_artist)

    def parse_artist_song_list(self, response):
        url_list = response.xpath('//*[@id="cmn_wrap"]/div[2]/div[1]/section[1]/table/tbody/tr[*]/td[1]/div[1]/a[1]/@href').extract()
        if url_list:
            for url in url_list:
                if url[0] != 'h':
                    url = "https://www.allmusic.com" + url
                    yield scrapy.Request(url, callback = self.parse_song)
        
    def parse_song(self, response):
        title = response.xpath('//*[@id="cmn_wrap"]/div/div[2]/header/hgroup/h1/text()').extract()[0].strip()
        song_url = response.url
        performer = response.xpath('//*[@id="cmn_wrap"]/div/div[2]/header/hgroup/h2/span/a/text()').extract()
        performer_url = response.xpath('//*[@id="cmn_wrap"]/div/div[2]/header/hgroup/h2/span/a/@href').extract()
        if performer_url:
            for url in performer_url:
                if url[0] != 'h':
                    url = "https://www.allmusic.com" + url
                    yield scrapy.Request(url, callback = self.parse_artist)        
        composer = response.xpath('//*[@class="song-composer"]/a/text()').extract()
        composer_url = response.xpath('//*[@class="song-composer"]/a/@href').extract()
        if composer_url:
            for url in composer_url:
                if url[0] != 'h':
                    url = "https://www.allmusic.com" + url
                    yield scrapy.Request(url, callback = self.parse_artist)   
        release_year = response.xpath('//*[@id="cmn_wrap"]/div/div[1]/section[1]/div[2]/div/p[1]/text()').extract()
        genres =  response.xpath('//*[@class = "song_genres"]/div[@class = "middle"]/a//text()').extract()
        styles =  response.xpath('//*[@class = "song_styles"]/div[@class = "middle"]/a//text()').extract()
        moods =  response.xpath('//*[@class = "song_moods"]/div[@class = "middle"]/a//text()').extract()
        themes =   response.xpath('//*[@class = "song_themes"]/div[@class = "middle"]/a//text()').extract()
        in_album =  response.xpath('//*[@class = "artist-album"]/div[@class = "title"]/a/text()').extract()
        album_url = response.xpath('//*[@class = "artist-album"]/div[@class = "title"]/a/@href').extract()
        time =  response.xpath('//*[@class = "time"]//text()').extract()
        if time:
            for item in time:
                item = item.strip()

        song_obj = song_Item()
        song_obj['title'] = title
        song_obj['url'] = song_url
        if performer:
            song_obj['performer'] = performer
        if performer_url:
            song_obj['performer_url'] = performer_url
        if composer:
            song_obj['composer'] = composer
        if composer_url:
            song_obj['composer_url'] = composer_url
        if release_year:
            song_obj['release_year'] = release_year
        if genres:
            song_obj['genres'] = genres
        if styles:
            song_obj['styles'] = styles
        if moods:
            song_obj['moods'] = moods
        if themes:
            song_obj['themes'] = themes
        if in_album:
            song_obj['in_album'] = clean(in_album)
        if album_url:
            song_obj['album_url'] = album_url
        # if time:
        #     song_obj['time'] = clean(time)

        album_url_list =  response.xpath('//*[@id="cmn_wrap"]/div/div[2]/section/table/tbody/tr[*]/td[4]/div[2]/a/@href').extract()
        if album_url_list:
            for url in album_url_list:
                if url[0] != 'h':
                    url = "https://www.allmusic.com" + url
                    yield scrapy.Request(url, callback = self.parse_album)   

        yield song_obj

    def parse_album(self, response):
        song_url_list = response.xpath('//*[@id="cmn_wrap"]/div[2]/div[1]/section[2]/div/table/tbody/tr[*]/td[4]/div[1]/a/@href').extract()
        if song_url_list:
            for url in song_url_list:
                if url[0] != 'h':
                    url = "https://www.allmusic.com" + url
                    yield scrapy.Request(url, callback = self.parse_song)   


    def parse_artist(self, response):
        name = response.xpath('//*[@class="artist-name"]//text()').extract()[0].strip()
        url = response.url
        biography = response.xpath('//*[@class="biography"]/span/text()').extract()
        active_years = response.xpath('//*[@class="active-dates"]/div//text()').extract()
        born_in = response.xpath('//*[@class="birth"]/div/a/text()').extract()
        genres =  response.xpath('//*[@class="genre"]/div/a//text()').extract()
        styles =  response.xpath('//*[@class="styles"]/div/a//text()').extract()
        aliases =  response.xpath('//*[@class="aliases"]/div/div//text()').extract()
        group_members = response.xpath('//*[@class="group-members"]/div/a[*]/span/text()').extract()
        group_members_url = response.xpath('//*[@class="group-members"]/div/a[*]/@href').extract()

        artist_obj = artist_Item()
        artist_obj['name'] = name
        artist_obj['url'] = url
        if biography:
            artist_obj['biography'] = biography
        if active_years:
            artist_obj['active_years'] = active_years
        if born_in:
            artist_obj['born_in'] = born_in
        if genres:
            artist_obj['genres'] = genres
        if styles:
            artist_obj['styles'] = styles
        if aliases:
            artist_obj['aliases'] = aliases
        if group_members:
            artist_obj['group_members'] = group_members
            for url in group_members_url:
                url = "https://www.allmusic.com" + url
                yield scrapy.Request(url, callback = self.parse_artist)
            artist_obj['group_members_url'] = group_members_url

        yield artist_obj

        yield scrapy.Request(url + '/songs', callback = self.parse_artist_song_list)
