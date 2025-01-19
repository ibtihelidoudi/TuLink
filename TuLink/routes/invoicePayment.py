from fastapi import APIRouter,Depends,HTTPException
from config.db import conn,SessionLocal ,get_db
from models.index import startUps,invoicePayments,users,startUpRepresentatives,serviceProviders,bookings
from schemas.index import InvoicePayment
from sqlalchemy.orm import  Session
from sqlalchemy import select,alias,literal_column
from auth.auth import isValid,isAdmin,isServiceProvider,isAdmin,isStartUpRepresentativeOrAdmin,isServiceProviderOrAdmin


invoicePayment= APIRouter()

@invoicePayment.get("/invoicePayment/",dependencies=[Depends(isAdmin)])
async def read_data(db: Session = Depends(get_db)):
    try:
        result = db.execute(
        select(bookings.c.dateAppointement,
               bookings.c.dateCreationRequest,
               bookings.c.lastDateModifiedRequest,
               bookings.c.startingTime,
               bookings.c.durationInMinit,
               serviceProviders.c.id,
               invoicePayments.c.typeOfPayment,
               serviceProviders.c.priceMin,
               startUpRepresentatives.c.id,
               startUpRepresentatives.c.idStartUp,
               startUps.c.nameStartUp,
               startUps.c.localisation,
               invoicePayments.c.id,) 
        .join(invoicePayments, invoicePayments.c.idBooking == bookings.c.id) 
        .join(serviceProviders, bookings.c.idServiceProvider == serviceProviders.c.id) 
        .join(startUpRepresentatives, bookings.c.idRepresentative == startUpRepresentatives.c.id)  
        .join(startUps, startUps.c.id == startUpRepresentatives.c.idStartUp) 

        ).fetchall()

        invoicePayments_list = [{ "serviceProvider": {"id":row[5],"priceMin":row[7]},
        "startUpRepresentatives":{"id":row[8]},
        "booking": {"dateAppointement":row[0],"dateCreationRequest":row[1],"lastDateModifiedRequest":row[2],"startingTime":row[3],"durationInMinit":row[4]},
        "startUp":{"id":row[9],"nameStartUp":row[10],"localisation":row[11]} ,
        "invoicePayment": {"id":row[12],"typeOfPayment":row[6]},
        "commission":'15%', 
        "amount":row[4] * row[7] * 85/100
    }
        for row in result
        ]
        return {"invoicePayments_list": invoicePayments_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving invoice: {e}")

@invoicePayment.get("/invoicePayment/{id}",dependencies=[Depends(isValid)])
async def read_data(id: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(
        invoicePayments.select() 
        .where(invoicePayments.c.id == id)
        ).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="invoicePayments not found")
        result = db.execute(
        select(bookings.c.dateAppointement,
               bookings.c.dateCreationRequest,
               bookings.c.lastDateModifiedRequest,
               bookings.c.startingTime,
               bookings.c.durationInMinit,
               serviceProviders.c.id.label("serviceProviderId"),
               invoicePayments.c.typeOfPayment,
               serviceProviders.c.priceMin,
               startUpRepresentatives.c.id.label("startUpRepresentativesId"),
               startUpRepresentatives.c.idStartUp,
               startUps.c.nameStartUp,
               startUps.c.localisation,
               invoicePayments.c.typeOfPayment,
) 
        .join(invoicePayments, invoicePayments.c.idBooking == bookings.c.id)  
        .join(serviceProviders, bookings.c.idServiceProvider == serviceProviders.c.id) 
        .join(startUpRepresentatives, bookings.c.idRepresentative == startUpRepresentatives.c.id)  
        .join(startUps, startUps.c.id == startUpRepresentatives.c.idStartUp) 
        .where(invoicePayments.c.id == id)
        ).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        invoicepayment ={ "serviceProvider": {"id":result.serviceProviderId,"priceMin":result.priceMin,},
        "startUpRepresentatives":{"id":result.startUpRepresentativesId,},
        "booking": {"dateAppointement":result.dateAppointement,"dateCreationRequest":result.dateCreationRequest,"lastDateModifiedRequest":result.lastDateModifiedRequest,"startingTime":result.startingTime,"durationInMinit":result.durationInMinit},
        "startUp":{"id":result.idStartUp,"nameStartUp":result.nameStartUp,"localisation":result.localisation} ,
        "invoicePayment": {"typeOfPayment":result.typeOfPayment,"id":id},
        "commission":'15%',
        "amount":result.durationInMinit * result.priceMin * 85/100,
        }
    

        
        return {"invoicePayment": invoicepayment}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving invoicePayments: {e}")


@invoicePayment.delete("/invoicePayment/{id}",dependencies=[Depends(isValid)])
async def delete_data(id:int, db: Session = Depends(get_db)):
    try:
        invoicePayment_db = db.execute(invoicePayments.select().where(invoicePayments.c.id == id)).fetchone()
        if invoicePayment_db is None:
            raise HTTPException(status_code=404, detail="invoicePayment not found")       
        db.execute(invoicePayments.delete().where(invoicePayments.c.id == id))
        db.commit()
        return {"message": f"invoicePayment with id {id} has been deleted successfully"}

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"Error deleting invoicePayment: {e}")


@invoicePayment.post("/invoicePayment/",dependencies=[Depends(isStartUpRepresentativeOrAdmin)])
async def write_data(invoicePayment: InvoicePayment, db: Session = Depends(get_db)):
    try:
      result=db.execute(invoicePayments.insert().values(
      typeOfPayment=invoicePayment.typeOfPayment,
      idBooking=invoicePayment.idBooking
      ))     
      db.commit()
      return {"message": "invoicePayment created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inserting invoicePayment: {e}")

@invoicePayment.put("/invoicePayment/{id}",dependencies=[Depends(isStartUpRepresentativeOrAdmin)])
async def modif_data(id:int,invoicePayment:InvoicePayment, db: Session = Depends(get_db)):
    try:
        invoicePayment_db = db.execute(invoicePayments.select().where(invoicePayments.c.id == id)).fetchone()
        if invoicePayment_db is None:
            raise HTTPException(status_code=404, detail="InvoicePayment not found")
        db.execute(invoicePayments.update()
        .where(invoicePayments.c.id == id)
        .values(
        typeOfPayment=invoicePayment.typeOfPayment
        ))
        
        db.commit()
        updated_invoice = db.execute(invoicePayments.select().where(invoicePayments.c.id == id)).fetchone()

        return {"invoicePayment":{"id": updated_invoice[0], "typeOfPayment": updated_invoice[1], "idBooking": updated_invoice[2]}}

    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"Error updating invoicePayment: {e}")


