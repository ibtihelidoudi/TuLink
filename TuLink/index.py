from fastapi import FastAPI 
from routes.index import admin,serviceProvider,booking,startUp,startUpRepresentative,invoicePayment
from auth.auth import router

app=FastAPI()
app.include_router(admin)
app.include_router(router)
app.include_router(serviceProvider)
app.include_router(startUp)
app.include_router(booking)
app.include_router(startUpRepresentative)
app.include_router(invoicePayment)
