from datetime import timedelta,datetime
from typing import Annotated
from config.db import conn,SessionLocal ,get_db
from sqlalchemy.orm import  Session
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status 

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from models.index import users

router=APIRouter(
    prefix='/auth',
    tags  =['auth']
)

SECRET_KEY='197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM='HS256'
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

class Token(BaseModel):
    access_token:str
    token_type  :str

def get_dbb():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close
db_dependency= Annotated[Session,Depends(get_dbb)]

@router.post("/token",response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
db:db_dependency):
   print(form_data.username,form_data.password)
   user=authenticate_user(form_data.username,form_data.password,db)
   if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')
   token=create_access_token(user.email,user.id,user.role,timedelta(minutes=20))
   return {'access_token':token,'token_type':'bearer'}

def authenticate_user(username:str,password:str,db):
    user = db.execute(users.select()
                           .where(users.c.email == username)).fetchone()
    if not user:
        print("if not user")
        return False
    if not bcrypt_context.verify(password,user.password):
        print("if not bcrypt_context.verify(password,user.password)")
        return False
    return user

def create_access_token(username:str,user_id:int,role:str,expires_delta:timedelta):
    encode={'sub':username,'id':user_id,'role':role}
    expires=datetime.utcnow()+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithm=[ALGORITHM])
        username:str=payload.get('sub')
        user_id:int=payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')
        return {'username':username,'id':user_id}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')

async def isAdmin(token:Annotated[str,Depends(oauth2_bearer)]):

        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        role:str=payload.get('role')
        if  role !='admin':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='only for admin')
      
        else:
             return payload
        
  
async def isStartUpRepresentative(token:Annotated[str,Depends(oauth2_bearer)]):
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        role:str=payload.get('role')
        if  role !='startUpRepresentative':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='only for admin')
      
        else:
             return payload
async def isServiceProvider(token:Annotated[str,Depends(oauth2_bearer)]):
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        role:str=payload.get('role')
        if  role !='serviceProvider':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='only for serviceProvider')
      
        else:
             return payload

async def isServiceProviderOrAdmin(token:Annotated[str,Depends(oauth2_bearer)]):
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        role:str=payload.get('role')
        if  role !='serviceProvider' and role !='admin' :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='only for serviceProvider and admin')
        else:
             return payload

async def isStartUpRepresentativeOrAdmin(token:Annotated[str,Depends(oauth2_bearer)]):
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        role:str=payload.get('role')
        if  role !='startUpRepresentative' and role !='admin' :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='only for startUpRepresentative and admin')
        else:
             return payload
async def isValid(token:Annotated[str,Depends(oauth2_bearer)]):
        try:
           payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
           return payload
    
        except JWTError:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')

    