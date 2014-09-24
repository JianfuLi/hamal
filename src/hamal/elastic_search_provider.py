# -*- coding: utf-8 -*-
import logging
from elasticsearch import Elasticsearch

logger = logging.getLogger('hamal.ElasticSearchProvider')


class ElasticSearchProvider(object):
    """
    elasticsearch全文搜索SDK
    """

    def __init__(self, hosts=None):
        self._es = Elasticsearch(hosts)

    def insert(self, index, doc_type, doc):
        """
        :arg schema: es的_index
        :arg table: es的_type
        :arg row: 需要更新的doc
        """
        res = self._es.index(index, doc_type, doc, doc['id'])
        return res['created']

    def update(self, index, doc_type, doc):
        """
        :arg schema: es的_index
        :arg table: es的_type
        :arg row: 需要更新的doc
        """
        self._es.index(index, doc_type, doc, doc['id'])
        return True


    def delete(self, index, doc_type, doc):
        """
        :arg schema: es的_index
        :arg table: es的_type
        :arg row: 需要更新的doc
        """
        res = self._es.delete(index, doc_type, doc['id'])
        return res['found']
