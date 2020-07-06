import unittest
from sources.hackernews.api import HackerNewsApi
from sources.hackernews.plugin import HackerNews
class TestHackerNews(unittest.TestCase):
    def test_get_hackernews_articles_by_api(self):
        hn  = HackerNewsApi()
        articles = hn.get_topstories(limit=2)          
        self.assertNotEqual(0,len(articles),"No articles returned")
    
    def test_get_hackernews_articles(self):
        hn  = HackerNews()
        articles = hn.get_articles(limit=2)        
        self.assertNotEqual(0,len(articles),"No articles returned")

if __name__=='__main__':
    unittest.main()