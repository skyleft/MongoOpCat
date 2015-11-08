#!/usr/bin/env python
#-*- coding:utf-8 -*-

from abc import ABCMeta,abstractmethod

class AbstractSender(object):
    __metaclass__ = ABCMeta

    @staticmethod
    def getObjectId(oplog):
        id = None
        #check if o2 is existed, means it is an update operation
        o2 = oplog.get('o2')
        if o2 is not None:
            id = o2.get('_id')
        #check if o is existed, means it is an insert or delete operation
        if id is None:
            id = oplog['o'].get('_id')
        return id

    @abstractmethod
    def startSend(self, oplog):
        pass