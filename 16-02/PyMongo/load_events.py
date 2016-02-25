import bson
import pymongo
from datetime import datetime
from random import random
conn = pymongo.MongoClient()
db = conn.event_db

for i in xrange(0,100):
    hour = int(random()*24)
    minute = int(random()*60)
    sec = int(random()*60)
    event = {
        "_id": bson.ObjectId(),
        "host": "127.0.0.1",
        "time":  datetime(2000,10,10,hour,minute,sec),
        "path": "/apache_pb.gif",
        "referer": "[http://www.example.com/start.html](http://www.example.com/start.html)",
        "user_agent": "Mozilla/4.08 [en] (Win98; I ;Nav)"
    }
    db.events.insert(event, w=1)
