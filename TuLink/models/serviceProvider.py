from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Float,Integer,String,Text,Enum
from  config.db import meta

# Table pour ServiceProvider
serviceProviders = Table(
    'serviceProvider', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer),  # Clé étrangère vers 'users'
    Column('positionFieldOfExpertise', String(255)),
    Column('description', Text),
    Column('academicBackground', Text),
    Column('professionalExperience', Text),
    Column('linkedinLink', String(255)),
    Column('portefolioWebSiteLink', String(255)),
    Column('status', Enum('accepted', 'waiting', 'rejected')),
    Column('priceMin', Float) #price per minute 

    ) 
    