from sources import SourceOfNews
from .config import REQUEST_HEADERS
from enum import Enum
import requests
import logging

class FieldMapper(Enum):
    HEADLINE = 'title'
    LINK = 'url_overridden_by_dest'

class Reddit(SourceOfNews):
    BASE_URIS = ['https://www.reddit.com/r/news']
    def __init__(self):
        super().__init__('reddit')
    def get_articles(self, topic=None, limit=25):        
        if topic is None:
            request_url = f'{self.BASE_URIS[0]}/.json'
        else:
            request_url = f'{self.BASE_URIS[0]}/search.json?restrict_sr=on&limit={limit}&q={topic}'        
        logging.info(f'REDDIT DATA URL {request_url}')
        try:            
            req = requests.get(request_url, headers =REQUEST_HEADERS)
        except requests.exceptions.ConnectionError as e:
            raise e
        
        if req.status_code != 200:
            if req.status_code == 401:
                raise Exception('Unauthorized/API Key invalid')
        return self.parse_data(req.json())

    def parse_data(self, data):
        items = []
        articles = data.get('data',{}).get('children')
        
        for article in articles:
            article_data = article.get('data')
            items.append({
                'headline': article_data.get(FieldMapper.HEADLINE.value),
                'link': article_data.get(FieldMapper.LINK.value),
                'source':self.name
            })
        return items
