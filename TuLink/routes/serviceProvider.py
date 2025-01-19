from fastapi import APIRouter,Depends,HTTPException
from config.db import conn,SessionLocal ,get_db
from models.index import serviceProviders,users
from schemas.index import User,ServiceProvider
from sqlalchemy.orm import  Session
from sqlalchemy import select
from auth.auth import bcrypt_context
from auth.auth import isValid,isAdmin,isServiceProvider,isAdmin,isStartUpRepresentativeOrAdmin,isServiceProviderOrAdmin

serviceProvider= APIRouter()

@serviceProvider.get("/serviceProvider/",dependencies=[Depends(isValid)])
async def read_data(db: Session = Depends(get_db)):
    try:
        result = db.execute(
        select(users, serviceProviders)  
        .join(serviceProviders, users.c.id == serviceProviders.c.user_id)  # Jointure sur role_id
        ).fetchall()
        print(result)
        users_list = [{"id": row[0],
        "name": row[1],
        "surname": row[2],
        "email": row[3],
        "password": row[4],
        "role": row[5],
        'positionFieldOfExpertise': row[8],
        'description': row[9],
        'academicBackground': row[10],
        'professionalExperience': row[11],
        'linkedinLink': row[12],
        'portefolioWebSiteLink': row[13],
        'status': row[14],
        'priceMin': row[15]

       
    }
        for row in result
        ]
        return {"users": users_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {e}")

@serviceProvider.get("/serviceProvider/{id}",dependencies=[Depends(isStartUpRepresentativeOrAdmin)])
async def read_data(id: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(
        select(users, serviceProviders) 
        .join(serviceProviders, users.c.id == serviceProviders.c.user_id)  
        .where(users.c.id == id)
        ).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        print(result)
        user ={
        "id": result.id, 
        "name": result.name, 
        "surname": result.surname,  
        "email": result.email,  
        "password": result.password, 
        "role": result.role,
        "positionFieldOfExpertise": result.positionFieldOfExpertise, 
        "academicBackground": result.academicBackground,  
        "professionalExperience": result.professionalExperience, 
        "linkedinLink": result.linkedinLink,  
        "portefolioWebSiteLink": result.portefolioWebSiteLink, 
        "status": result.status,  
        "priceMin" : result.priceMin

}
        
        return {"user": user}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {e}")

@serviceProvider.put("/serviceProvider/{id}",dependencies=[Depends(isServiceProviderOrAdmin)])
async def modif_data(id:int,serviceProvider:ServiceProvider, db: Session = Depends(get_db)):
    try:
        user_db = db.execute(users.select().where(users.c.id == id)).fetchone()
        
        if user_db is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.execute(users.update()
        .where(users.c.id == id)
        .values(
        name=serviceProvider.name,
        surname=serviceProvider.surname,
        email=serviceProvider.email,
        password=bcrypt_context.hash(serviceProvider.password),
        role="serviceProvider"  
        ))
        db.execute(serviceProviders.update()
        .where(serviceProviders.c.user_id == id).values(
        user_id=id,
        positionFieldOfExpertise=serviceProvider.positionFieldOfExpertise,
        academicBackground=serviceProvider.academicBackground,
        description=serviceProvider.description,
        professionalExperience=serviceProvider.professionalExperience,
        linkedinLink=serviceProvider.linkedinLink,
        portefolioWebSiteLink=serviceProvider.portefolioWebSiteLink,
        status=serviceProvider.status,
        priceMin=serviceProvider.priceMin

      ))
        db.commit()
        updated_user = db.execute(users.select().where(users.c.id == id)).fetchone()
        return {"user": {"id": updated_user[0], "name": updated_user[1], "email": updated_user[2], "password": updated_user[3]}}

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"Error updating user: {e}")


@serviceProvider.delete("/serviceProvider/{id}",dependencies=[Depends(isAdmin)])
async def delete_data(id:int, db: Session = Depends(get_db)):
    try:
       
        user_db = db.execute(users.select().where(users.c.id == id)).fetchone()

        if user_db is None:
            raise HTTPException(status_code=404, detail="User not found")
        

        db.execute(serviceProviders.delete().where(serviceProviders.c.user_id == id))
 
        db.execute(users.delete().where(users.c.id == id))

        db.commit()
        return {"message": f"User with id {id} has been deleted successfully"}

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"Error deleting user: {e}")


@serviceProvider.post("/serviceProvider/")
async def write_data(serviceProvider: ServiceProvider, db: Session = Depends(get_db)):
    try:
      print("allo",serviceProvider) 
      password_hashed=bcrypt_context.hash(serviceProvider.password)        
      result=db.execute(users.insert().values(
      name=serviceProvider.name,
      surname=serviceProvider.surname,
      email=serviceProvider.email,
      password=password_hashed,
      role="serviceProvider"  
      ))
      print("good")
      db.execute(serviceProviders.insert().values(
      user_id=result.inserted_primary_key[0],
      positionFieldOfExpertise=serviceProvider.positionFieldOfExpertise,
      academicBackground=serviceProvider.academicBackground,
      description=serviceProvider.description,
      professionalExperience=serviceProvider.professionalExperience,
      linkedinLink=serviceProvider.linkedinLink,
      portefolioWebSiteLink=serviceProvider.portefolioWebSiteLink,
      status="waiting",
      priceMin=serviceProvider.priceMin
      ))
      db.commit()
      return {"message": "User created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inserting user: {e}")

