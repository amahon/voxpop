

import celery
from celery.utils.log import get_task_logger


app = celery.Celery('comment_stored')
app.config_from_object('config.celeryconfig')


@app.task
def comment_stored(_id):

    print _id



@app.task()
def process_comment(comment):

    article = db['article'].find_one({'web_url': comment['_metadata']['query_params']['url']})

    comment_body = BeautifulSoup(comment['commentBody']).get_text()

    tokens = nltk.word_tokenize(comment_body)

    n_tokens = 0
    mean_valance = 0.0
    mean_affect = 0.0
    mean_dominance = 0.0
    for token in tokens:
        if token in _affective_words:
            n_tokens = n_tokens + 1
            mean_valance = mean_valance + float(_affective_words[token]['V.Mean.Sum'])
            mean_affect = mean_affect + float(_affective_words[token]['A.Mean.Sum'])
            mean_dominance = mean_dominance + float(_affective_words[token]['D.Mean.Sum'])
    mean_valance = mean_valance / n_tokens
    mean_affect = mean_affect / n_tokens
    mean_dominance = mean_dominance / n_tokens

    sentiment = {
        'tokens': tokens,
        'tokens_count': len(tokens),
        'VMeanSum': mean_valance,
        'AMeanSum': mean_affect,
        'DMeanSum': mean_dominance,
    }

    db['comment'].update({'_id': ObjectId(comment['_id'])}, {"$set": {"sentiment": sentiment}}, upsert=False)