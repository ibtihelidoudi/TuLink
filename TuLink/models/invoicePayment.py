from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String,Float
from  config.db import meta

# Table pour InvoicePayment
invoicePayments = Table(
    'invoicePayment', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('typeOfPayment', String(50)),
    Column('idBooking', Integer))
