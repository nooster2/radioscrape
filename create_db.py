from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

from mapping import Base

engine = create_engine('sqlite:////home/alex/PythonProjekte/radioscrape/db.sqlite3', echo=True)

#Create Schema
Base.metadata.create_all(engine)
