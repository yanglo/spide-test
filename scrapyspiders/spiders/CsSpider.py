# -*- coding: utf-8 -*-
# spider for cs website

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import time
import re

from scrapyspiders.spiders.BaseSpider import SpiderMixin


class CsSpider(CrawlSpider, SpiderMixin):
    name = "cs"
    allowed_domains = ["www.cs.com.cn"]
    start_urls = [
        "http://www.cs.com.cn/xwzx/hg/",
        "http://www.cs.com.cn/ssgs/gsxw/",
    ]

    def next_page(self, response):
        tail_pattern = '/index_%s.html'

        page = re.findall('\/index_(\d)\.html$', response.url)
        if page:
            assert len(page) == 1
            page = int(page[0])
            if page >= 9:
                return None
            else:
                url = re.sub("\/index_\d\.html$", tail_pattern % (page + 1), response.url)
        else:
            url = response.url.strip('/') + tail_pattern % 1

        return url

    def parse(self, response):
        pq = response.pq
        reqs = []
        for each in pq("div.subwrapper > div.subleftbox > div.column-box > ul > li > a").items():
            url = each.attr['href']
            reqs.append(Request(url, self.parse_detail))

        nextpage = self.next_page(response)
        if nextpage:
            reqs.append(Request(nextpage, priority=-5))

        return reqs

    def parse_detail(self, response):
        ISOTIMEFORMAT = '%Y-%m-%d %H:%M'

        pq = response.pq

        dt = response.pq('div.subleftbox > div.column-box > div.column-sub > span.ctime01')
        dt.remove('span.ctime')

        content = pq('div.subleftbox > div.column-box > div.Dtext')
        content.remove('style')

        item = {
            'url': response.url,
            'ScrapeDate': time.strftime(ISOTIMEFORMAT, time.localtime()),
            'PubDate': dt.text(),
            'channel': pq('div.subwrapper > div.content.linkblack > a').eq(-1).text(),
            'title': pq('div.subleftbox > div.column-box > h1').text(),
            'source': pq('div.subleftbox > div.column-box > div.column-sub > em').eq(-1).text(),
            'content': content.text(),
        }
        return item