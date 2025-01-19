from pydantic import BaseModel
from datetime import datetime

class Booking(BaseModel):
    idRepresentative        :int = None
    idServiceProvider       :int = None
    dateAppointement        :datetime
    dateCreationRequest     :datetime
    lastDateModifiedRequest :datetime
    startingTime            :datetime
    durationInMinit         :int

