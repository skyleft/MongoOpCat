#!/usr/bin/env python
# -*- coding:utf-8 -*-

from AbstractSender import AbstractSender
from MongoOpCat.utils.BsonUtils import restoreFromOplog


class StdOutSenderCat(AbstractSender):

    """
    This is a sample sender cat, which will monitor the mongodb oplog
    when there are new mongo operation
    it just simply print the log to console
    """

    #override the update method
    def update(self, ns, ts, id, mod, raw, **kw):
        super(StdOutSenderCat, self).update(self, ns, ts, id, mod, raw, **kw)
        print "[%s] update on %s, %s" % (ts.as_datetime(),ns,restoreFromOplog(raw))

    #override the delete method
    def delete(self, ns, ts, id, raw, **kw):
        super(StdOutSenderCat, self).delete(self, ns, ts, id, raw, **kw)
        print "[%s] delete on %s, %s" % (ts.as_datetime(),ns,restoreFromOplog(raw))

    #override the noop method
    def noop(self, ts):
        super(StdOutSenderCat, self).noop(self, ts)

    #override the db_declare method
    def db_declare(self, ns, ts, **kw):
        super(StdOutSenderCat, self).db_declare(self, ns, ts, **kw)

    #override the insert method
    def insert(self, ns, ts, id, obj, raw, **kw):
        super(StdOutSenderCat, self).insert(self, ns, ts, id, obj, raw, **kw)
        print "[%s] insert on %s, %s" % (ts.as_datetime(),ns,restoreFromOplog(raw))




