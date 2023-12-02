from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteSchema(BaseModel):
    title : str
    content : str

class NoteResponse(BaseModel):
    id : int
    title : str
    content : str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S')
    }
        
class UserSchema(BaseModel):
    username : str
    email : str
    password : str

class UserResponse(BaseModel):
    id : int
    username : str
    email : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str