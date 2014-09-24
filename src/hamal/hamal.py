# -*- coding: utf-8 -*-

import logging
import json

from hamal.setting import *
from hamal.listener import Listener

logger = logging.getLogger('hamal.Hamal')


class Hamal(object):
    """
    Binlog搬动工，转换binlog日志格式为全文搜索的文档格式，并同步数据到全文搜索服务器中
    """

    def __init__(self):
        """
        初始化binlog监听器
        """
        logger.debug(
            "初始化Binlog事件监听器，connection_settings: %r, server_id: %r， blocking:%r, resume_stream: %r",
            json.dumps(CONNECTION_SETTINGS), SERVER_ID, BLOCKING, RESUME_STREAM
        )
        self._listener = Listener(CONNECTION_SETTINGS, SERVER_ID, BLOCKING, RESUME_STREAM)


    def hauling(self):
        """
        接收binlog流
        """
        logger.info("开始接收数据...")
        self._listener.accept(self._process)

    def _process(self, schema, table, method, columns):
        """
        :arg schema: 发生变更的mysql数据库名
        :arg table: 发生变更的mysql表名
        :arg method: 变更事件，INSERT或UPDATE或DELETE
        :arg columns: 变更后最新的字段字典，格式为{"column1":"value1","column2":"value2"}
        """
        if schema not in PROJECTIONS.keys():
            logger.debug("发生变更的数据库为: %r，不在配置节中，忽略该事件", schema)
            return

        if table not in PROJECTIONS[schema].keys():
            logger.debug("发生变更的表为: %r，不在数据库%r的配置节中，忽略该事件", table, schema)
            return

        doc = PROJECTIONS[schema][table](columns)

        logger.debug("数据原结构：%r", json.dumps(columns))
        logger.debug("转换成文档：%r", json.dumps(doc))

        self._send_request(schema, table, method, doc)

    def _send_request(self, schema, table, method, doc):
        if method == 'INSERT':
            PROVIDER.insert(schema, table, doc)
        elif method == 'UPDATE':
            PROVIDER.update(schema, table, doc)
        elif method == 'DELETE':
            PROVIDER.delete(schema, table, doc)
