from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String,Enum
from  config.db import meta

# Table pour User
users = Table(
    'user', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255)),
    Column('surname', String(255)),
    Column('email', String(255), unique=True),
    Column('password', String(255)),
    Column('role', Enum('admin', 'serviceProvider', 'startUpRepresentative'))
)