#!/usr/bin/env python
# -*- coding:utf-8 -*-

from AbstractSender import AbstractSender
from MongoOpCat.utils.BsonUtils import restoreFromOplog
import os

class FSSenderCat(AbstractSender):

    """
    Another sample sender, it will write the oplog json to file when there is new operation on mongo
    """

    def __init__(self,path):
        if path:
            if os.path.exists(path):
                self.path = path
                self.fs = None
            else:
                raise ValueError('the path must be existed.')
        else:
            raise ValueError('must provide a path')


    def fsSync(self,ts,raw):
        fsName = "%s.mop" % (str(ts.as_datetime()).split(' ')[0],)
        if self.fs is None:
            self.fs = open(os.path.join(self.path,fsName),'a+')
        else:
            if self.fs.name <> fsName:
                self.fs.flush()
                self.fs.close()
                self.fs = open(os.path.join(self.path,fsName),'a+')
            else:
                pass
        self.fs.write("%s%s" % (restoreFromOplog(raw),os.linesep))

    #override the update method
    def update(self, ns, ts, id, mod, raw, **kw):
        super(FSSenderCat, self).update(self, ns, ts, id, mod, raw, **kw)
        self.fsSync(ts,raw)

    #override the delete method
    def delete(self, ns, ts, id, raw, **kw):
        super(FSSenderCat, self).delete(self, ns, ts, id, raw, **kw)
        self.fsSync(ts,raw)

    #override the noop method
    def noop(self, ts):
        super(FSSenderCat, self).noop(self, ts)

    #override the db_declare method
    def db_declare(self, ns, ts, **kw):
        super(FSSenderCat, self).db_declare(self, ns, ts, **kw)

    #override the insert method
    def insert(self, ns, ts, id, obj, raw, **kw):
        super(FSSenderCat, self).insert(self, ns, ts, id, obj, raw, **kw)
        self.fsSync(ts,raw)




