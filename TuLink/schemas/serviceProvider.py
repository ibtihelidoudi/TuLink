from schemas.index import User
 
class ServiceProvider(User):
   positionFieldOfExpertise:str
   description             :str
   academicBackground      :str
   professionalExperience  :str
   linkedinLink            :str
   portefolioWebSiteLink   :str
   status                  :str 
   priceMin                :float