
import json
import logging
import datetime


import celery
from celery.utils.log import get_task_logger

import requests

from .db import db, store_document

NYT_ARTICLE_API_KEY = '6b386fbb1141bc111298f599fe611bab:1:49052537'
NYT_COMMUNITY_API_KEY = '3cd7b97dd0c16c8523ea7ccba7f5fdd1:13:49052537'

logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)

app = celery.Celery('api')
app.config_from_object('config.celeryconfig')


def articles_api_request(params):
    params.update({'api-key': NYT_ARTICLE_API_KEY})
    logger.debug('Querying NYT Article Search API v2')
    logger.debug('{}'.format(params))
    return requests.get(
            'http://api.nytimes.com/svc/search/v2/articlesearch.json',
            params=params)


def community_api_request(params):
    params.update({'api-key': NYT_COMMUNITY_API_KEY})
    logger.debug('Querying NYT Community API')
    logger.debug('{}'.format(params))
    return requests.get(
            'http://api.nytimes.com/svc/community/v2/comments/url/exact-match.json',
            params=params)


# TODO: Abstract the following two methods as they contain lots of similar structure

@app.task
def fetch_articles(params, metadata={}):
    from .article import article_stored

    r = articles_api_request(params)
    metadata.update({'query_params': params})

    n_hits = r.json()['response']['meta']['hits']
    if not n_hits:
        return

    if not 'page' in params:
        n_queries = n_hits/10
        logger.info('Generating {} more API Queries to retrieve {} Articles'.format(n_queries, n_hits))
        for page in range(1, n_queries):
            my_params = params.copy()
            my_params.update({'page': page})
            fetch_articles.delay(my_params, metadata=metadata)

    for doc in r.json()['response']['docs']:
        article_stored.delay(store_document(doc, 'article', metadata=metadata))


@app.task
def fetch_comments(params, metadata={}):
    from .comment import comment_stored

    r = community_api_request(params)
    metadata.update({'query_params': params})

    n_hits = r.json()['results']['totalCommentsFound']
    if not n_hits:
        return

    if not 'page' in params:
        n_queries = n_hits/25
        logger.info('Generating {} more API Queries to retrieve {} Comments'.format(n_queries, n_hits))
        for page in range(1, n_queries):
            my_params = params.copy()
            my_params.update({'page': page})
            fetch_comments.delay(my_params, metadata=metadata)

    for doc in r.json()['results']['comments']:
        comment_stored.delay(store_document.delay(doc, 'comment', metadata=metadata))


