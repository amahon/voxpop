
import logging

import celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)

app = celery.Celery('review')
app.config_from_object('config.celeryconfig')

from .article import process_article
from .comment import process_comment

@app.task
def review_stored_articles():
    for article in db['article'].find():
        process_article.delay(article)


@app.task
def review_stored_comments():
    for comment in db['comment'].find():
        process_comment.delay(comment)
