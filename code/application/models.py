import flask
from application import db
from wtforms.fields import TextAreaField
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document):
       
    name  =   db.StringField( unique=True )
    mail       =   db.StringField( unique=True )
    password    =   db.StringField( )

class Customer(db.Document):
    SSN = db.StringField(unique=True)
    cname  =   db.StringField()
    age      =   db.StringField()
    address  =   db.StringField()
    state     =   db.StringField()
    city  =   db.StringField()

class Account(db.Document):
    cid = db.StringField(unique=True)
    acid  =   db.StringField(unique=True)
    actype      =   db.StringField()
    damount  =   db.StringField()
    Depositedamount=db.IntField()
    

  
