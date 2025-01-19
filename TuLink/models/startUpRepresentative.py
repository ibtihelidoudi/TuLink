from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String
from  config.db import meta

# Table pour StartUpRepresentative
startUpRepresentatives = Table(
    'startUpRepresentative', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer),  # Clé étrangère vers 'users'
    Column('idStartUp', Integer)
)
