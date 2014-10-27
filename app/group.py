

from bson.code import Code
import pymongo

mongo_client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = mongo_client.nyt_sentiment_db

token_group = Code(open('../mapreduce/token_group.js', 'r').read())

result = db.comment.group(
    key={'_metadata.query_params.url': 1},
    condition={},
    initial={},
    reduce=token_group
)
for document in result:
    print document