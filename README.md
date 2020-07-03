# newshound

This is a toy app using the FastAPI library. It's shows

+ load a plugin to pull in news from an API, wip is a plugin for hackernews
+ authenticate, and then use the generated jwt token for subsequent calls (typo11/secret)
+ go to /docs to see the swagger-link auto generated ui 
+ can extend content to feed into tbot telegram app, always want to generalise the source from reddit subs to something else and this things plugin pattern would be perfect.
+ can extend to cache the feed use lru_cache
+ see how to add claims based authentication where claims is encoding in the jwt payload (like done on the payspace demo)

todo
+ build a UI (spa? react? or go with mvc core?)
