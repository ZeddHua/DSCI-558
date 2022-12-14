# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from allmusic.items import *
import json


class AllmusicPipeline:
    def process_item(self, item, spider):
        if isinstance(item, genre_Item):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.file_genre.write(line)
        elif isinstance(item, song_Item):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.file_song.write(line)
        elif isinstance(item, artist_Item):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.file_artist.write(line)
        return item

    def open_spider(self, spider):
        self.file_genre = open('genre.jsonl', 'w')
        self.file_song = open('song.jsonl', 'w')
        self.file_artist = open('artist.jsonl', 'w')

    def close_spider(self, spider):
        self.file_genre.close()
        self.file_song.close()
        self.file_artist.close()