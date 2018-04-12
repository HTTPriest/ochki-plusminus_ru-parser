# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ImagePathPipeline(object):
    def process_item(self, item, spider):
        image_path = item['images'][0]['path']
        item['images'] = image_path
        return item
