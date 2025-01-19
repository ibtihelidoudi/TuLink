from pydantic import BaseModel

class InvoicePayment(BaseModel):
    id               :int = None
    typeOfPayment    :str
    idBooking        :int = None
    