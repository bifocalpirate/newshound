from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from .config import LRU_SIZE
import importlib
import time
import logging
from abc import ABC, abstractmethod


class SourceOfNews(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_articles(self, topic=None, limit=25):
        raise NotImplementedError

    @abstractmethod
    def parse_data(self, request_data):
        raise NotImplementedError

class NewsManager:
    def __init__(self, providers):
        self.providers = []
        for provider, provider_path in providers.items():
            module = importlib.import_module(provider_path)            
            provider_class = getattr(module, provider)
            if not ("get_articles" in dir(provider_class) and callable(getattr(provider_class,"get_articles"))):
                raise NotImplementedError("Must implement get_articles method in provider.")
            self.providers.append(provider_class())  # add the instance

    @lru_cache(maxsize=LRU_SIZE)
    def fetch_articles(self, topic=None):
        articles = []
        threads = []
        with ThreadPoolExecutor(max_workers=len(self.providers)) as executor:
            for provider in self.providers:
                threads.append(executor.submit(provider.get_articles, topic))
        for task in as_completed(threads):
            articles.extend(task.result())        
        return articles
