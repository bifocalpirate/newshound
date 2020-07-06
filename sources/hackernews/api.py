import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import logging

class HackerNewsApi:
    TOPSTORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"        
    REQUEST_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}
    
    def get_content_url(self, article_id):
        return f"https://hacker-news.firebaseio.com/v0/item/{article_id}.json"

    def __init__(self):
        pass

    def make_request(self, request_url):
        try:
            req = requests.get(request_url, headers=self.REQUEST_HEADERS)
            return req
        except requests.exceptions.ConnectionError as e:
            raise e
    
    def get_topstories(self, limit=20):
        topstories = self.make_request(self.TOPSTORIES_URL)
        article_ids = json.loads(topstories.content)    
        article_urls = list(map(self.get_content_url, article_ids[1:limit]))
        results = []
        threads = []
        with ThreadPoolExecutor(max_workers=5) as executor:                    
            for url in article_urls:                
                threads.append(executor.submit(self.make_request, url))        
        for task in as_completed(threads):
            results.append(json.loads(task.result().content.decode('utf-8')))            
        return results