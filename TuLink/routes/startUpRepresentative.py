from fastapi import APIRouter,Depends,HTTPException
from config.db import conn,SessionLocal ,get_db
from models.index import startUpRepresentatives,users
from schemas.index import User,StartUpRepresentative
from sqlalchemy.orm import  Session
from sqlalchemy import select
from auth.auth import bcrypt_context
from auth.auth import isAdmin,isServiceProvider,isAdmin,isStartUpRepresentativeOrAdmin,isServiceProviderOrAdmin


startUpRepresentative= APIRouter()


@startUpRepresentative.get("/startUpRepresentative/",dependencies=[Depends(isAdmin)])
async def read_data(db: Session = Depends(get_db)):
    try:
      
        result = db.execute(
        select(users, startUpRepresentatives)  
        .join(startUpRepresentatives, users.c.id == startUpRepresentatives.c.user_id)  # Jointure sur role_id
        ).fetchall()

        users_list = [{"id": row[0],
        "name": row[1],
        "surname": row[2],
        "email": row[3],
        "password": row[4],
        "role": row[5],
        "idStartUp": row[8]
       
    }
        for row in result
        ]
        return {"users": users_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {e}")

@startUpRepresentative.get("/startUpRepresentative/{id}",dependencies=[Depends(isAdmin)])
async def read_data(id: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(
        select(users, startUpRepresentatives) 
        .join(startUpRepresentatives, users.c.id == startUpRepresentatives.c.user_id)  
        
        .where(users.c.id == id)
        ).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        user ={
        "id": result.id,  
        "name": result.name,  
        "surname": result.surname,  
        "email": result.email,  
        "password": result.password, 
        "role": result.role,  
        "idStartUp":result.idStartUp
}
        
        return {"user": user}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {e}")

@startUpRepresentative.put("/startUpRepresentative/{id}",dependencies=[Depends(isAdmin)])
async def modif_data(id:int,startUpRepresentative:StartUpRepresentative, db: Session = Depends(get_db)):
    try:
        user_db = db.execute(users.select().where(users.c.id == id)).fetchone()
        
        if user_db is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.execute(users.update()
        .where(users.c.id == id)
        .values(
        name=startUpRepresentative.name,
        surname=startUpRepresentative.surname,
        email=startUpRepresentative.email,
        password=startUpRepresentative.password,
        role="startUpRepresentative"  
        ))
        db.execute(startUpRepresentatives.update()
        .where(startUpRepresentatives.c.user_id == id).values(
        user_id=id,
        idStartUp=startUpRepresentative.idStartUp
      ))
        db.commit()
        updated_user = db.execute(users.select().where(users.c.id == id)).fetchone()
        return {"user": {"id": updated_user[0], "name": updated_user[1], "email": updated_user[2], "password": updated_user[3]}}

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"Error updating user: {e}")


@startUpRepresentative.delete("/startUpRepresentative/{id}",dependencies=[Depends(isAdmin)])
async def delete_data(id:int, db: Session = Depends(get_db)):
    try:
        user_db = db.execute(users.select().where(users.c.id == id)).fetchone()
        if user_db is None:
            raise HTTPException(status_code=404, detail="User not found")

        
        db.execute(startUpRepresentatives.delete().where(startUpRepresentatives.c.user_id == id))
        db.execute(users.delete().where(users.c.id == id))

        db.commit()
        return {"message": f"User with id {id} has been deleted successfully"}

    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"Error deleting user: {e}")


@startUpRepresentative.post("/startUpRepresentative/")
async def write_data(startUpRepresentative: StartUpRepresentative, db: Session = Depends(get_db)):
    try:
      password_hashed=bcrypt_context.hash(startUpRepresentative.password)        
      result=db.execute(users.insert().values(
      name=startUpRepresentative.name,
      surname=startUpRepresentative.surname,
      email=startUpRepresentative.email,
      password=password_hashed,
      role="startUpRepresentative"  
      ))
      db.execute(startUpRepresentatives.insert().values(
      user_id=result.inserted_primary_key[0],
      idStartUp=startUpRepresentative.idStartUp

      ))
      db.commit()
      return {"message": "startUpRepresentative created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inserting user: {e}")

