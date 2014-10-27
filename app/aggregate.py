

from bson.code import Code
import pymongo

mongo_client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = mongo_client.nyt_sentiment_db

token_map = Code(open('../mapreduce/token_map.js', 'r').read())
token_reduce = Code(open('../mapreduce/token_reduce.js', 'r').read())


for article in db.article.find():
    comments = db.comment.find({'_metadata.query_params.url': article["web_url"]})
    if comments.count():
        result = db.comment.map_reduce(
            token_map,
            token_reduce,
            {'reduce': "article.{}.comment_tokens".format(article['_id'])},
            query={'_metadata.query_params.url': article["web_url"]}
        )
        for document in result.find():
            print document