from sources import SourceOfNews

from sources.exceptions import InvalidAPIKey, APIKeyMissing
from sources.config import REQUEST_TIMEOUT
from .config import API_KEY
from enum import Enum
import requests
import logging

class FieldMapper(Enum):
    HEADLINE = 'title'
    LINK = 'url'

class NewsApi(SourceOfNews):
    BASE_URI = 'https://newsapi.org/v2/everything?'
    def __init__(self, API_KEY=API_KEY):
        super().__init__('newsapi')
        if API_KEY is None:
            raise ApiKeyMissing(self.__class__.__name__)
        self.API_KEY = API_KEY

    def get_articles(self, topic=None):
        q_param = 'general' if topic is None else topic
        request_url = f'{self.BASE_URI}q={q_param}&apiKey={self.API_KEY}'
        logging.info(request_url)
        
        try:            
            req =requests.get(request_url, timeout=REQUEST_TIMEOUT)
            req.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise e
        if req.status_code != 200:
            if req.status_code == 401:
                raise InvalidAPIKey(self.__class__.__name__)
        return self.parse_data(req.json())

    
    def parse_data(self, data):
        posts = []
        logging.info(data)
        articles = data.get('articles',{})        
        for article in articles:
            posts.append({
                'headline':article.get(FieldMapper.HEADLINE.value),
                'link':article.get(FieldMapper.LINK.value),
                'source':self.name
            })
        return posts
        
    
