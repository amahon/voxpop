

import celery
from celery.utils.log import get_task_logger


app = celery.Celery('article')
app.config_from_object('config.celeryconfig')



from .db import db


@app.task
def article_stored(_id):
    process_article.delay(_id)


@app.task
def process_article(_id):
    from .api import fetch_comments
    article = db.article.find_one({'_id': _id})
    fetch_comments.delay({
            'url': article['web_url']
        }, metadata={
            'article_id': article['_id']
        })