from sqlalchemy import Table,Column,DateTime
from sqlalchemy.sql.sqltypes import Integer,String
from  config.db import meta


# Table pour Booking
bookings = Table(
    'booking', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('idRepresentative', Integer),  # Clé étrangère vers 'start_up_representatives'
    Column('idServiceProvider', Integer),  # Clé étrangère vers 'service_providers'
    Column('dateAppointement', DateTime),
    Column('dateCreationRequest', DateTime),
    Column('lastDateModifiedRequest', DateTime),
    Column('startingTime', DateTime),
    Column('durationInMinit', Integer)
)