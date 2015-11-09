#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient
from MongoOpCat.sender.AbstractSender import AbstractSender
from MongoOpCat.sender.StdOutSenderCat import StdOutSenderCat

class Configuration(object):

    def __init__(self):
        self.mongov = None
        self.databasev = None
        self.collectionv = None
        self.timeInterval = 1.0
        self.ifStartNow = True
        self.senders = [StdOutSenderCat(),]

    def ready(self):
        if self.mongov is not None and self.senders is not None and len(self.senders) > 0:
            return True
        else:
            return False

    #mongo you want to monitor
    def mongo(self,mongov):
        if mongov and isinstance(mongov, MongoClient):
            self.mongov = mongov
            return self
        else:
            raise ValueError('Mongo connection is not provided.')

    #database you want to monitor
    def database(self,databasev):
        if databasev:
            self.databasev = databasev
        return self

    #collection you want to monitor
    def collection(self,collectionv):
        if collectionv:
            if self.databasev:
                self.collectionv = collectionv
            else:
                raise ValueError('Must provide database name before you provide collection name')
        return self

    #time interval
    def interval(self,timeInterval):
        if timeInterval:
            self.timeInterval = timeInterval
        return self

    #if start now
    def startNow(self,ifStartNow):
        if ifStartNow:
            self.ifStartNow = ifStartNow
        return self

    #sender
    def sender(self,nSender):
        if nSender and isinstance(nSender,AbstractSender):
            self.senders.append(nSender)
        return self
