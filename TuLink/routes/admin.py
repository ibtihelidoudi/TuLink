from fastapi import APIRouter,Depends,HTTPException
from config.db import conn,SessionLocal ,get_db
from models.index import startUpRepresentatives,users
from schemas.index import User,StartUpRepresentative
from sqlalchemy.orm import  Session
from sqlalchemy import select
from auth.auth import bcrypt_context
from auth.auth import isAdmin,isServiceProvider,isAdmin,isStartUpRepresentativeOrAdmin,isServiceProviderOrAdmin

admin= APIRouter()

@admin.post("/admin/")
async def write_data(user: User, db: Session = Depends(get_db)):
    try:
      result=db.execute(users.insert().values(
      name=user.name,
      surname=user.surname,
      email=user.email,
      password=bcrypt_context.hash(user.password),
      role="admin"  
      ))
     
      db.commit()
      return {"message": "user created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inserting user: {e}")

