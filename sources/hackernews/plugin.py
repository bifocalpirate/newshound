from sources import SourceOfNews

from sources.exceptions import InvalidAPIKey, APIKeyMissing
from sources.config import REQUEST_TIMEOUT
from .api import HackerNewsApi
from enum import Enum
import logging

class FieldMapper(Enum):
    HEADLINE = 'title'
    LINK = 'url'

class HackerNews(SourceOfNews):    
    def __init__(self):
        super().__init__('hackernews')

    def get_news(self, topic=None, limit=25):
        hapi = HackerNewsApi()
        articles = hapi.get_topstories(limit)        
        return self.parse_data(articles)

    def parse_data(self, data):        
        posts = []        
        for article in data:                        
            posts.append({
                'headline': article[FieldMapper.HEADLINE.value],
                'link': article[FieldMapper.LINK.value],
                'source': self.name
            })
        return posts
