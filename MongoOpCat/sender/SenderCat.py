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

