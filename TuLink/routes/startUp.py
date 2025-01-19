from fastapi import APIRouter,Depends,HTTPException
from config.db import conn,SessionLocal ,get_db
from models.index import startUps
from schemas.index import StartUp
from sqlalchemy.orm import  Session
from sqlalchemy import select
from auth.auth import isAdmin,isServiceProvider,isAdmin,isStartUpRepresentativeOrAdmin,isServiceProviderOrAdmin


startUp= APIRouter()


@startUp.get("/startUp/",dependencies=[Depends(isAdmin)])
async def read_data(db: Session = Depends(get_db)):
    try:
        result = db.execute(
        startUps.select()  
        ).fetchall()
        startUps_list = [{"id": row[0],
        "nameStartUp": row[1],
        "localisation": row[2]
    }
        for row in result
        ]
        return {"startUps": startUps_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving startUps: {e}")

@startUp.get("/startUp/{id}",dependencies=[Depends(isAdmin)])
async def read_data(id: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(
        startUps.select() 
        .where(startUps.c.id == id)
        ).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="startUp not found")

        print(result)
        startUp ={
        "id": result.id,
        "nameStartUp": result.nameStartUp,
        "localisation": result.localisation
}
        
        return {"startUp": startUp}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving startUps: {e}")

@startUp.put("/startUp/{id}",dependencies=[Depends(isAdmin)])
async def modif_data(id:int,startUp:StartUp, db: Session = Depends(get_db)):
    try:
        startUp_db = db.execute(startUps.select().where(startUps.c.id == id)).fetchone()
        
        if startUp_db is None:
            raise HTTPException(status_code=404, detail="StartUp not found")
        db.execute(startUps.update()
        .where(startUps.c.id == id)
        .values(
        nameStartUp=startUp.nameStartUp,
        localisation=startUp.localisation
        ))
       
        db.commit()
        updated_startUp = db.execute(startUps.select().where(startUps.c.id == id)).fetchone()
        return {"startUp": {"id": updated_startUp[0], "nameStartUp": updated_startUp[1], "localisation": updated_startUp[2]}}

    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"Error updating StartUp: {e}")


@startUp.delete("/startUp/{id}",dependencies=[Depends(isAdmin)])
async def delete_data(id:int, db: Session = Depends(get_db)):
    try:
  
        startUp_db = db.execute(startUps.select().where(startUps.c.id == id)).fetchone()

        if startUp_db is None:
            raise HTTPException(status_code=404, detail="StartUp not found")

        db.execute(startUps.delete().where(startUps.c.id == id))

        db.commit()
        return {"message": f"startUp with id {id} has been deleted successfully"}

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"Error deleting startUp: {e}")


@startUp.post("/startUp/",dependencies=[Depends(isAdmin)])
async def add_data(startUp: StartUp, db: Session = Depends(get_db)):
    try:
      result=db.execute(startUps.insert().values(
      nameStartUp=startUp.nameStartUp,
      localisation=startUp.localisation
     
      ))
     
      db.commit()
      return {"message": "startUp created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inserting startUp: {e}")

