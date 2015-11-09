#!/usr/bin/env python
# -*- coding:utf-8 -*-

def restoreFromOplog(raw):
    if raw and raw['op']:
        if 'u'==raw['op']:
            return "db.%s.update(%s,%s)" % (str(raw['ns']).replace("u'","'").split('.')[-1],str(raw['o2']).replace("u'","'"),str(raw['o']).replace("u'","'"))
        elif 'i'==raw['op']:
            return "db.%s.insert(%s)" % (str(raw['ns']).replace("u'","'").split('.')[-1],str(raw['o']).replace("u'","'"))
        elif 'd'==raw['op']:
            return "db.%s.remove(%s)" % (str(raw['ns']).replace("u'","'").split('.')[-1],str(raw['o']).replace("u'","'"))
        else:
            #ignore all the other operation
            return None
    else:
        return None
