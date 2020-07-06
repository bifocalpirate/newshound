from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from .config import LRU_SIZE
import importlib
import time
import logging


class SourceOfNews:
    def __init__(self, name):
        self.name = name

    def get_articles(self, query=None):
        raise NotImplementedError

    def parse_data(self, request_data):
        raise NotImplementedError


class NewsManager:
    def __init__(self, providers):
        self.providers = []
        for provider, provider_path in providers.items():
            module = importlib.import_module(provider_path)
            print(f'provider path {provider_path}')
            provider_class = getattr(module, provider)
            self.providers.append(provider_class())  # add the instance

    @lru_cache(maxsize=LRU_SIZE)
    def fetch_news(self, topic=None):
        articles = []
        threads = []
        logging.info('setting up threads...')
        with ThreadPoolExecutor(max_workers=len(self.providers)) as executor:
            for provider in self.providers:
                threads.append(executor.submit(provider.get_news, topic))
        for task in as_completed(threads):
            articles.extend(task.result())
        print(articles)
        return articles
