#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient, CursorType
from pymongo.errors import AutoReconnect
import re
import time

from MongoOpCat.sender.SenderCat import SenderCat


class WatchCat(object):
    def __init__(self, database=None, collection=None, timeInterval=1.0, connection=None, ifStartNow=True, sender = None):
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

        if sender is None:
            raise ValueError('Sender is none.')
        self.sender = sender

        if ifStartNow:
            self.startWatch()



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
                        self.sender.startSend(op)
                    time.sleep(self.timeInterval)
                    if not cursor.alive:
                        break
            except AutoReconnect:
                time.sleep(self.timeInterval)




if __name__ == '__main__':
    WatchCat(connection=MongoClient('localhost',27017),sender=SenderCat())
