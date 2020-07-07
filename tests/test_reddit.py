import unittest
from sources.reddit import Reddit

class TestReddit(unittest.TestCase):    
    
    def test_get_reddit_articles(self):
        reddit = Reddit()
        articles = reddit.get_articles(limit=2)        
        self.assertNotEqual(0,len(articles),"No articles returned")

if __name__=='__main__':
    unittest.main()