MongoOpCat
======

Overview
========

MongoOpCat is a subscribe service for mongodb oplog, support for Slave-Master and ReplicaSets.
You can use it to implement incremental backup or some other log functionality.

Requirements
============

* Python 2.7
* Works on Linux, Windows, Mac OSX, BSD

Install
=======

The quickest and easiest way

    pip install MongoOpCat


Usage Example
=======
    from MongoOpCat.monitor.MonitorCat import MonitorCat
    from MongoOpCat.conf.Configuration import Configuration
    from MongoOpCat.sender.StdOutSenderCat import StdOutSenderCat
    from MongoOpCat.sender.FSSenderCat import FSSenderCat
    from pymongo import MongoClient

    cat = MonitorCat(Configuration().mongo(MongoClient('mongodb://127.0.0.1',27017))
                         .database("testdb").collection("testcollection").interval(2).sender(StdOutSenderCat())
                         .sender(FSSenderCat('.')))

This code will monitor testcolletion of testdb on 127.0.0.1:27017, if there is new CRUD operation on it
it will print the operation description to the console(StdOutSenderCat) and write the mongodb command to
the mop file(FSSenderCat).

If you want to do more things, just extends MongoOpCat.sender.AbstractSender, and override the insert,delete,update
method to do what you want.

Support
==================
http://andy-cheung.me
@im@andy-cheung.me
