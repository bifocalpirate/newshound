import unittest
from sources.newsapi import NewsApi

class TestNewsApi(unittest.TestCase):    
    
    def test_get_newsapi(self):
        hn  = NewsApi("c2d941c74c144421945618d97a458144") #get a seperate key?
        articles = hn.get_articles(limit=2)        
        self.assertNotEqual(0,len(articles),"No articles returned")

if __name__=='__main__':
    unittest.main()