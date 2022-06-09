# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import re
import scrapy
import hashlib
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class CastoramaPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.Castorama

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        item['characteristics'] = self.process_characteristics(item)
        item['_id'] = item['photos'][0]['checksum']

        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            None

        return item

    def process_characteristics(self, item):
        ''' Список списков где первое слово ХАРАКТЕРИСТИКИ, а потом непосредственно характеристики'''
        char_df = []

        flag = True
        for line in item['characteristics']:
            if re.findall(r'\w', line):
                ''' int '''
                try:
                    inp = int(re.search(r'\b.*\b', line)[0])
                except ValueError:
                    ''' float '''
                    try:
                        inp = float(re.search(r'\b.*\b', line)[0])
                    except ValueError:
                        inp = re.search(r'\b.*\b', line)[0]

                if flag:
                    char_df.append([inp])
                    flag = False
                else:
                    char_df[-1].append(inp)
                    flag = True


class CastoramaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]

        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_url_hash = hashlib.shake_256(request.url.encode()).hexdigest(5)
        title = item['title'].split(' ')[0]
        image_filename = f'full/{title}/{image_url_hash}_{image_url_hash[3]}.jpg'

        return image_filename