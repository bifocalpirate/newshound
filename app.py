from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import logging
#from fastapi.responses import ORJSONResponse

from dotenv import load_dotenv
load_dotenv()

from sources.source import SourceOfNews, NewsManager
from sources.exceptions import InvalidAPIKey, APIKeyMissing
from datetime import timedelta

from auth.sec import User, fake_decode_token, \
    get_current_active_user, create_access_token, UserInDB, \
    authenticate_user
from fake_users import fake_users_db


from typing import Optional
import json
import os

from auth.sec import Token

providers = {
    'Reddit' : 'sources.reddit', #class name: 'location of class'
    'NewsApi' : 'sources.newsapi'
}

news_manager = NewsManager(providers)
app=FastAPI()

########################################################
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    logging.info(f"{form_data.username}. {form_data.password}")
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:            
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,\
                            detail= "Incorrect username or password",\
                            headers = {'WWWW-Authenticate':'Bearer'},
                            )
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES")))
    access_token = create_access_token(
        data={"sub":user.username}, expires_delta=access_token_expires
    )    
    return {"access_token":access_token, "token_type":"bearer"}
  
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner":current_user.username}]

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/")
async def ping():
    return {"version":"0.1"}

@app.get("/protected")
async def protected(token:str=Depends(oauth2_scheme)):
    return {"token":token}

@app.get("/news")
async def news(query:str=None):
    try:
        return news_manager.fetch_news(query)
    except InvalidAPIKey as e:
        provider = e.provider
        raise HTTPException(status_code=401, detail=f'{provider} : Invalid API key')
    except APIKeyMissing as e:
        provider= e.provider
        raise HTTPException(status_code=401, detail=f'{provider} : API key not configured')
