# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapyspiders.org/en/latest/topics/item-pipeline.html


class ScrapyDemoPipeline(object):
    def process_item(self, item, spider):
        return item
