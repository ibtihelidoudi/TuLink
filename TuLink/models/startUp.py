from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String
from  config.db import meta

# Table pour StartUp
startUps = Table(
    'startUp', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('nameStartUp', String(255)),
    Column('localisation', String(255)),

)
