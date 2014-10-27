
from .db import db

def empty_collections(collections=['article', 'comment']):
    import pymongo
    for collection in collections:
        db[collection].remove()

