from fastapi import APIRouter,Depends,HTTPException
from config.db import conn,SessionLocal ,get_db
from models.index import bookings
from schemas.index import Booking
from sqlalchemy.orm import  Session
from sqlalchemy import select
from auth.auth import isValid,isAdmin,isServiceProvider,isStartUpRepresentative,isAdmin,isStartUpRepresentativeOrAdmin,isServiceProviderOrAdmin


booking= APIRouter()

@booking.get("/booking/",dependencies=[Depends(isAdmin)])
async def read_data(db: Session = Depends(get_db)):
    try:
        result = db.execute(
        bookings.select()  
        ).fetchall()
        bookings_list = [{"id": row[0],
        "idRepresentative": row[1],
        "idServiceProvider": row[2],
        "dateAppointement": row[3],
        "dateCreationRequest": row[4],
        "lastDateModifiedRequest": row[5],
        "startingTime": row[6],
        "durationInMinit": row[7],

    }
        for row in result
        ]
        return {"bookings": bookings_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving bookings: {e}")

@booking.get("/booking/{id}",dependencies=[Depends(isValid)])
async def read_data(id: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(
        bookings.select() 
        .where(bookings.c.id == id)
        ).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="booking not found")

        print(result)
        booking ={
        "idRepresentative":result.idRepresentative,
        "idServiceProvider":result.idServiceProvider,
        "dateAppointement":result.dateAppointement,
        "dateCreationRequest":result.dateCreationRequest,
        "lastDateModifiedRequest":result.lastDateModifiedRequest,
        "startingTime":result.startingTime,
        "durationInMinit":result.durationInMinit
}
        
        return {"booking": booking}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving bookings: {e}")

@booking.put("/booking/{id}",dependencies=[Depends(isStartUpRepresentative)])
async def modif_data(id:int,booking:Booking, db: Session = Depends(get_db)):
    try:
        booking_db = db.execute(bookings.select().where(bookings.c.id == id)).fetchone()
        
        if booking_db is None:
            raise HTTPException(status_code=404, detail="booking not found")
        db.execute(bookings.update()
        .where(bookings.c.id == id)
        .values(
        idRepresentative=booking.idRepresentative,
        idServiceProvider=booking.idServiceProvider,
        dateAppointement=booking.dateAppointement,
        dateCreationRequest=booking.dateCreationRequest,
        lastDateModifiedRequest=booking.lastDateModifiedRequest,
        startingTime=booking.startingTime,
        durationInMinit=booking.durationInMinit

        ))
       
        db.commit()
        updated_booking = db.execute(bookings.select().where(bookings.c.id == id)).fetchone()
        return {"booking": {"id": updated_booking[0], "namebooking": updated_booking[1], "localisation": updated_booking[2]}}

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"Error updating booking: {e}")


@booking.delete("/booking/{id}",dependencies=[Depends(isStartUpRepresentativeOrAdmin)])
async def delete_data(id:int, db: Session = Depends(get_db)):
    try:
  
        booking_db = db.execute(bookings.select().where(bookings.c.id == id)).fetchone()

        if booking_db is None:
            raise HTTPException(status_code=404, detail="booking not found")

        db.execute(bookings.delete().where(bookings.c.id == id))

        db.commit()
        return {"message": f"booking with id {id} has been deleted successfully"}

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"Error deleting booking: {e}")


@booking.post("/booking/",dependencies=[Depends(isStartUpRepresentativeOrAdmin)])
async def add_data(booking: Booking, db: Session = Depends(get_db)):
    try:
      result=db.execute(bookings.insert().values(
        idRepresentative=booking.idRepresentative,
        idServiceProvider=booking.idServiceProvider,
        dateAppointement=booking.dateAppointement,
        dateCreationRequest=booking.dateCreationRequest,
        lastDateModifiedRequest=booking.lastDateModifiedRequest,
        startingTime=booking.startingTime,
        durationInMinit=booking.durationInMinit
     
      ))
     
      db.commit()
      return {"message": "booking created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inserting booking: {e}")

