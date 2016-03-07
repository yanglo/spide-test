# -*- coding: utf-8 -*-
import demjson
import six
import chardet
import lxml.html
import lxml.etree

from pyquery import PyQuery


class PyqueryMiddleware(object):

    def pretty_unicode(self, string):
        """
        Make sure string is unicode, try to decode with utf8, or unicode escaped string if failed.
        """
        if isinstance(string, six.text_type):
            return string
        try:
            return string.decode("utf8")
        except UnicodeDecodeError:
            return string.decode('Latin-1').encode('unicode_escape')

    def encoding(self, txt, response):
        # content is unicode
        if isinstance(txt, six.text_type):
            return 'unicode'

        if hasattr(response, 'encoding') and response.encoding:
            return response.encoding

        # Fallback to auto-detected encoding.
        encoding = chardet.detect(txt)['encoding']

        if encoding and encoding.lower() == 'gb2312':
            encoding = 'gb18030'

        return encoding or 'utf-8'

    def process_spider_input(self, response, spider):
        """Returns a PyQuery object of the response's content"""

        if response.meta.has_key('_splash_processed'):
            splash_setting = response.meta['_splash_processed']
            endpoint = splash_setting['endpoint']
            if endpoint in ['render.json', 'execute']:
                splash_key_html = spider._splash_json_key_html
                body = response.body_as_unicode() 
                splash_result = demjson.decode(body)
                if splash_result.has_key(splash_key_html):
                    body = splash_result[splash_key_html] 
                    setattr(response, 'splash_result', splash_result)
                else:
                    setattr(response, 'pq', None)
                    return
            elif endpoint in ['render.png','render.jpeg', 'render.har']:
                # do nothing and pyquery is unavailable
                setattr(response, 'pq', None)
                return
            elif endpoint in ['render.html']:
                # do nothing, continue
                body = response.body
        else:
            body = response.body

        if not body:
            setattr(response, 'pq', None)
            return

        enc = self.encoding(body, response)

        try:
            parser = lxml.html.HTMLParser(encoding=enc)
            elements = lxml.html.fromstring(body, parser=parser)
        except (LookupError, ) as e:
            # lxml would raise LookupError when encoding not supported
            # try fromstring without encoding instead.
            # on windows, unicode is not availabe as encoding for lxml
            elements = lxml.html.fromstring(body)
        if isinstance(elements, lxml.etree._ElementTree):
            elements = elements.getroot()
        pq = PyQuery(elements)
        if response.meta.get('_splash_processed'):
            pq.make_links_absolute( response.meta["_splash_processed"]["args"]["url"] )
        else:
            pq.make_links_absolute(response.url)

        setattr(response, 'pq', pq)
