from bs4 import BeautifulSoup
import urllib.request as urllib2
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mapping import Bayern3, LetzteSeite

#Connection zur Datenbank
engine = create_engine('sqlite:////home/alex/PythonProjekte/radioscrape/db.sqlite3') #, echo=True)
#Session zur Interaktion mit der Datenbank
Session = sessionmaker(bind=engine)
session = Session()

#zuletzt geparste URL als Startpunkt zum weitermachen
page = session.query(LetzteSeite).filter_by(id=1).first()
print(page.url)

#Ein Schleifendurchgang je URL
while True:
    try:
        html_page = urllib2.urlopen(page.url).read()
        #BeautifulSoup-Objekt aus Webseite
        soup = BeautifulSoup(html_page, 'html.parser')
        
        #Datum aus URL ziehen
        datum = page.url.split('_date-')[1].split('_hour-')[0]
        #Einträge finden
        zeiten = soup.find('dl', 'music_research').find_all('dt', 'time')
        for zeit in zeiten:
            datum_zeit = datetime.strptime(datum + 'T' + zeit.string,'%Y-%m-%dT%H:%M')
            li_titel_interpret = zeit.next_sibling.next_sibling.find('li', 'title')
            interpret = li_titel_interpret.span.string
            titel = li_titel_interpret.span.next_sibling.next_sibling.string
            
            session.add(Bayern3(datum_zeit=datum_zeit, interpret=interpret, titel=titel))
        
        print(datum_zeit.isoformat())
        #nächste URL
        page.url = 'http://www.br.de' + soup.find('p', 'playlist_navi_down').a.get('href')
        

    except AttributeError: #wird ausgelöst, wenn keine "nächste URL" gefunden werden kann
        print("AttributeError. Vermutlich letzte Seite erreicht: " + datum_zeit.isoformat())
        break
    
    except:
        raise
    
session.commit()
session.close()


