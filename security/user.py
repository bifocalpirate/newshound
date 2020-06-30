from pydantic import BaseModel
from typing import Optional
from fastapi import Depends

class User(BaseModel):
    username:str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

def fake_decode_token(token):
    return User(
            username=token+"fakedecoded", email="me@localhost.com", full_name="Bonnie Cacablanca"
        )


