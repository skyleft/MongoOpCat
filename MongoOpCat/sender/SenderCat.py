#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import time
from AbstractSender import AbstractSender


class SenderCat(AbstractSender):

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

    def noop(self, ts):
        print 'noop'

    def insert(self, ns, ts, id, obj, raw, **kw):
        print 'insert'
        time.sleep(1)

    def update(self, ns, ts, id, mod, raw, **kw):
        print 'update'

    def delete(self, ns, ts, id, raw, **kw):
        print 'delete'

    def command(self, ns, ts, cmd, raw, **kw):
        print 'command'

    def db_declare(self, ns, ts, **kw):
        print 'declare'