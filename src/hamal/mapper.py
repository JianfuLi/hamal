#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import datetime


class Mapper(object):
    @staticmethod
    def search_converter(fields):
        return {
            'id': fields['id'],
            'name': fields['name'],
            'create_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

