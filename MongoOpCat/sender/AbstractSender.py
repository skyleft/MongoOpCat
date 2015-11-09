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

    def startSend(self, oplog):
        ts = oplog['ts']
        id = self.getObjectId(oplog)
        self.all(ns=oplog['ns'], ts=ts, op=oplog['op'], id=id, raw=oplog)

    def all(self, ns, ts, op, id, raw):
        if op == 'n':
            self.noop(ts=ts)
        else:
            self.all(ns=ns, ts=ts, op=op, id=id, raw=raw)

    def all(self, ns, ts, op, id, raw):
        if op == 'i':
            self.insert(ns=ns, ts=ts, id=id, obj=raw['o'], raw=raw)
        elif op == 'u':
            self.update(ns=ns, ts=ts, id=id, mod=raw['o'], raw=raw)
        elif op == 'd':
            self.delete(ns=ns, ts=ts, id=id, raw=raw)
        elif op == 'c':
            self.command(ns=ns, ts=ts, cmd=raw['o'], raw=raw)
        elif op == 'db':
            self.db_declare(ns=ns, ts=ts, raw=raw)

    @staticmethod
    def noop(self, ts):
        pass

    @staticmethod
    def insert(self, ns, ts, id, obj, raw, **kw):
        pass

    @staticmethod
    def update(self, ns, ts, id, mod, raw, **kw):
        pass

    @staticmethod
    def delete(self, ns, ts, id, raw, **kw):
        pass

    @staticmethod
    def command(self, ns, ts, cmd, raw, **kw):
        pass

    @staticmethod
    def db_declare(self, ns, ts, **kw):
        pass