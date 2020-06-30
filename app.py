from fastapi import Depends,FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


#from fastapi.responses import ORJSONResponse

from dotenv import load_dotenv
load_dotenv()

from sources.source import SourceOfNews, NewsManager
from sources.exceptions import InvalidAPIKey, APIKeyMissing
from security.user import User, fake_decode_token
from fake_users import fake_users_db
from passlib.context import CryptContext
from pydantic import BaseModel
from jwt import PyJWTError
from typing import Optional
import json

SECRET_KEY = "5ef0fa23c8477b2c41a18690d4927f5cd9d5d295a42ea7416934a23e53f999e1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

providers = {
    'Reddit' : 'sources.reddit', #class name: 'location of class'
    'NewsApi' : 'sources.newsapi'
}

news_manager = NewsManager(providers)
app=FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(fake_db, username:str, password:str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token:str = Depends(oauth2_scheme)):
    user= fake_decode_token(token)
    if not user:
        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid authentication credentials",
                headers = {"WWW-Authenticate":"Bearer"},
            )
    return user

async def get_current_active_user(current_user:User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def fake_hash_password(password:str):
    return "fakehashed" + password


class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserInDB(User):
    hashed_password:str

def get_user(db, username:str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail= "Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail = "Incorrect username or password")
    return {"access_token":user.username, "token_type":"bearer"}
  
    
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
