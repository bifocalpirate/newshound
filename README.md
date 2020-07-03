# newshound

This is a toy app using the FastAPI library. It's shows

+ load a plugin to pull in news from an API
+ authenticate, and then use the generated jwt token for subsequent calls (typo11/secret)
+ go to /docs to see the swagger-link auto generated ui 

doing
+ complete wip for hackernews plugin

todo
+ store users in db (use sqlalchemy)
+ build a UI (spa? react? or go with mvc core?)
+ use praw instead of json url calls (like in tbot) then can send media content
+ can extend content to feed into tbot telegram app, always want to generalise the source from reddit subs to something else and this things plugin pattern would be perfect.
+ can extend to cache the feed use lru_cache
+ see how to add claims based authentication where claims is encoding in the jwt payload (like done on the payspace demo)


long term
+ authenticate using github/google federated login
+ android app consumes the api (very simple display list of items) and like articles
+ recomm engine maps likes to semantically analysed (or maybe just similarly tagged) articles
