#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient, CursorType
from pymongo.errors import AutoReconnect
import re
import time

from MongoOpCat.sender.StdOutSenderCat import StdOutSenderCat
from MongoOpCat.conf.Configuration import Configuration


class MonitorCat(object):
    def __init__(self, conf):
        if conf and conf.ready():
            collection = conf.collectionv
            database = conf.databasev
            timeInterval = conf.timeInterval
            connection = conf.mongov
            senders = conf.senders
            ifStartNow = conf.ifStartNow

            if collection is not None:
                if database is None:
                    raise ValueError('Unknown database name for collection %s' % (collection,))
                self.nsFilter = database + '.' + collection
            elif database is not None:
                self.nsFilter = re.compile(r'^%s\.' % database)
            else:
                self.nsFilter = None

            self.timeInterval = timeInterval

            if connection is None:
                raise ValueError('Mongo connection is not provided.')
            self.connection = connection

            if senders is None:
                raise ValueError('Senders is none.')
            self.senders = senders

            if ifStartNow:
                self.startWatch()
        else:
            raise SystemError('Configuration is not finished.')


    def startWatch(self):
        oplog = self.connection.local['oplog.rs']
        ts = oplog.find().sort('$natural', -1)[0]['ts']
        while True:
            if self.nsFilter is None:
                filter = {}
            else:
                filter = {'ns': self.nsFilter}
            filter['ts'] = {'$gt': ts}
            try:
                cursor = oplog.find(filter, cursor_type=CursorType.TAILABLE_AWAIT)
                while True:
                    for op in cursor:
                        for sender in self.senders:
                            sender.startSend(op)
                    time.sleep(self.timeInterval)
                    if not cursor.alive:
                        break
            except AutoReconnect:
                time.sleep(self.timeInterval)




if __name__ == '__main__':
    # import urllib
    # username = 'root'
    # password = urllib.quote_plus('root')
    cat = MonitorCat(Configuration().mongo(MongoClient('mongodb://127.0.0.1',27017)).database("mytest").collection("books").interval(2).sender(StdOutSenderCat()))
