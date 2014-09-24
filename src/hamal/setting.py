# -*- coding: utf-8 -*-
from hamal.mapper import Mapper
from hamal.elastic_search_provider import ElasticSearchProvider

CONNECTION_SETTINGS = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "passwd": "123456"
}
SERVER_ID = 3
BLOCKING = True
RESUME_STREAM = True

PROVIDER = ElasticSearchProvider({'host': 'localhost', 'port': 9200})
PROJECTIONS = {
    'rpl_test': {
        'search': Mapper.search_converter
    }
}