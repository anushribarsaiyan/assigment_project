from re import I
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from fastapi import Depends
from importlib import reload
import mod.crud as crud
from mod.models import address_book
from db import Base
from mod.crud import create_address,get_add,address_list,delete_address,update_address


#define sqlite connection url
SQLALCHEMY_DATABASE_URL = "sqlite:///./assigmnet.db"

# create new engine instance 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create sessionmaker 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
app = FastAPI()



from sqlalchemy.orm import Session
class  address_book(Base):
    __tablename__ = "Address_book"

    # fields 
    id = Column(Integer,primary_key=True, index=True)
    Address = Column(String(20))
    Near_place = Column(String(20))
    pincode = Column(Integer)
    condinates = Column(Integer)
"""
Session manages persistence operations for ORM-mapped objects.
Let's just refer to it as a database session for simplicity
"""


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/Createaddress")
def create_add(Address:str, near_place:str, pincode:int, codinates:int, db:Session = Depends(get_db)):
    addreess = create_address(db=db, Address=Address, near_place=near_place, pincode=pincode,codinates=codinates)
##return object created
    return {"addreess": addreess}


@app.get("/get_adress/{id}/") #id is a path parameter
def get_address(id:int, db:Session = Depends(get_db)):
    """
    the path parameter for id should have the same name as the argument for id
    so that FastAPI will know that they refer to the same variable
Returns a friend object if one with the given id exists, else null
    """
    get_data = get_add(db=db, id=id)
    return get_data



@app.get("/list_address")
def list_adresss(db:Session = Depends(get_db)):
    """
    Fetch a list of all address object
    Returns a list of objects
    """
    list_address = address_list(db=db)
    return list_address


@app.put("/update_address/{id}/") #id is a path parameter
def update_add(id:int, Address:str, near_place:str,pincode:int,codinates:int, db:Session=Depends(get_db)):
    #get adfress object from database
    db_address = get_address(db=db, id=id)
    #check if address object exists
    if db_address:
        updated_friend = update_address(db=db, id=id, Address=Address, near_place=near_place, pincode=pincode, codinates=codinates)
        return updated_friend
    else:
        return {"error": f"address with id {id} does not exist"}



@app.delete("/delete_address/{id}/") #id is a path parameter
def delete(id:int, db:Session=Depends(get_db)):
    #get adress object from database
    db_friend = get_add(db=db, id=id)
    #check if adress object exists
    if db_friend:
        return delete_address(db=db, id=id)
    else:
        return {"error": f"address with id {id} does not exist"}






























