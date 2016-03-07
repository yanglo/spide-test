# -*- coding: utf-8 -*-
# Base Spider schema
import copy


class SpiderMixin(object):

    _validator_param = {'allow_unknown': False}
    _base_schema = {
                'url':{'required': True, 'type':'string', 'empty': False, 'regex':'^https?://'},
                'ScrapeDate': {'required': True, 'type':'string', 'empty': False},
                'PubDate': {'required': True, 'type':'string', 'empty': False},
                'title': {'required': True, 'type':'string', 'empty': False},
                'channel': {'required': True, 'type':'string', 'empty': True},
                'content': {'required': True, 'type':'string', 'empty': True},
                'source': {'required': True, 'type':'string', 'empty': True},
            }


    def get_validator_schema(self):
        if hasattr(self, 'schema'):
            __schema = self.schema
        else:
            __schema = copy.deepcopy(self._base_schema)
        return __schema
