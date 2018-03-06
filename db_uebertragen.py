from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
  
#Neue DB
engine_neu = create_engine('sqlite:////home/alex/PythonProjekte/radioscrape/db.sqlite3', echo=True)
Session_neu = sessionmaker(bind=engine_neu)
session_neu = Session_neu()
Base_neu = declarative_base()

class Bayern3(Base_neu):
    __tablename__ = 'bayern3'
    
    id = Column(Integer, primary_key=True)
    datum_zeit = Column(DateTime)
    interpret = Column(String)
    titel = Column(String)

class LetzteSeite(Base_neu):
    __tablename__ = 'letzte_url'
    
    id = Column(Integer, primary_key=True)
    url = Column(String)
    
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

#Alte DB
# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine('sqlite:////home/alex/PythonProjekte/radioscrape/db_alt.sqlite3', echo=True)

Base_alt = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# mapped classes are now created with names by default
# matching that of the table name.
Bayern_alt = Base.classes.bayern3
Url_alt = Base.classes.letzte_url

Session_alt = sessionmaker(bind=engine_alt)
session_alt = Session_alt()
