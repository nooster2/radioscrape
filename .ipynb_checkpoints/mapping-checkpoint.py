from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class Bayern3(Base):
    __tablename__ = 'bayern3'
    
    id = Column(Integer, primary_key=True)
    datum_zeit = Column(DateTime)
    interpret = Column(String)
    titel = Column(String)

class LetzteSeite(Base):
    __tablename__ = 'letzte_url'
    
    id = Column(Integer, primary_key=True)
    url = Column(String)