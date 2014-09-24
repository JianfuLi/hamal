# -*- coding: utf-8 -*-
import logging
import json
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent)

logger = logging.getLogger('hamal.Listener')


class Listener(object):
    def __init__(self, connection_settings, server_id, blocking=True, resume_stream=True):
        self._stream = BinLogStreamReader(
            connection_settings=connection_settings,
            server_id=server_id,
            only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],
            blocking=blocking,
            resume_stream=resume_stream
        )

    def __del__(self):
        self._stream.close()

    def accept(self, callback):
        for log in self._stream:
            for row in log.rows:
                fields = {}
                method = ''
                if isinstance(log, DeleteRowsEvent):
                    fields = row["values"]
                    method = 'DELETE'
                elif isinstance(log, UpdateRowsEvent):
                    fields = row["after_values"]
                    method = 'UPDATE'
                elif isinstance(log, WriteRowsEvent):
                    method = 'INSERT'
                    fields = row["values"]

                logger.debug(
                    "捕获mysql %r事件, 值为: %r",
                    method, json.dumps(fields)
                )
                callback(log.schema, log.table, method, fields)
