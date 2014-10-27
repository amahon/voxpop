
from app.api import fetch_articles


fetch_articles.delay({
    'begin_date': '20140801',
    'end_date': '20141024',
    'fq': 'news_desk:("Opinion")'
})
