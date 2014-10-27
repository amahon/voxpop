#!/usr/bin/env python 

import tornado.autoreload
import tornado.ioloop
import tornado.web
import tornado.template

import pymongo

mongo_client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = mongo_client.nyt_sentiment_db

loader = tornado.template.Loader("templates")

class Articles(tornado.web.RequestHandler):

    def get(self):

        articles = db.article.find()

        articles_list = []

        for article in articles:
            article['comments'] = db.comment.find({'_metadata.query_params.url': article['web_url']})
            articles_list.append(article)

        self.write(loader.load("article.html").generate(
            articles=articles_list))

application = tornado.web.Application([
        (r"/", Articles),
    ])

if __name__ == "__main__":
    def fn():
        print "Hooked before reloading..."
    application.listen(9888)
    tornado.autoreload.add_reload_hook(fn)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()