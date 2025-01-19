from pydantic import BaseModel

class StartUp(BaseModel):
    idStartUp   :int = None
    nameStartUp :str 
    localisation:str