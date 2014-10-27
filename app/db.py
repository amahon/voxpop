
import logging

import celery
from celery.utils.log import get_task_logger

import pymongo
from pymongo.son_manipulator import SONManipulator
from bson.objectid import ObjectId

logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)

app = celery.Celery('db')
app.config_from_object('config.celeryconfig')

class ObjectIdManipulator(SONManipulator):

    def transform_incoming(self, son, collection):
        if u'_id' in son and isinstance(son[u'_id'], basestring):
            son[u'_id'] = ObjectId(son[u'_id'])
        return son

    def transform_outgoing(self, son, collection):
        if u'_id' in son:
            son[u'_id'] = str(son[u'_id'])
        return son

mongo_client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

db = mongo_client.nyt_sentiment_db
db.add_son_manipulator(ObjectIdManipulator())


@app.task
def store_document(doc, collection, metadata={}):
    doc.update({'_metadata': metadata})
    print(doc['_id'])
    doc_id = db[collection].save(doc)
    return doc_id

