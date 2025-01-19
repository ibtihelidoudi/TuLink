from pydantic import BaseModel

class User(BaseModel):
    id        :int =None
    name      :str
    surname   :str
    email     :str
    password  :str
    role      :str
