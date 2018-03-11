from bs4 import BeautifulSoup
import urllib.request as urllib2
import db

# Connection zur Datenbank
db.connect()
bayern3 = db.bayern3()

# zuletzt geparste URL als Startpunkt zum weitermachen
url = bayern3.get_letzte_url()

# Ein Schleifendurchgang je URL
while True:
    try:
        html_page = urllib2.urlopen(url).read()
        # BeautifulSoup-Objekt aus Webseite
        soup = BeautifulSoup(html_page, 'html.parser')
        
        # Datum aus URL ziehen
        datum = url.split('_date-')[1].split('_hour-')[0]
        zeiten = soup.find('dl', 'music_research').find_all('dt', 'time')
        # Einträge finden
        for zeit in zeiten:
            datum_zeit = datum + 'T' + zeit.string
            li_titel_interpret = zeit.next_sibling.next_sibling.find('li', 'title')
            interpret = li_titel_interpret.span.string
            titel = li_titel_interpret.span.next_sibling.next_sibling.string
            
            # In Datenbank eintragen
            bayern3.eintragen(datum_zeit, interpret, titel)

        # nächste URL
        url = 'http://www.br.de' + soup.find('p', 'playlist_navi_down').a.get('href')

    except AttributeError: # wird ausgelöst, wenn keine "nächste URL" gefunden werden kann
        print("AttributeError. Letzte Seite erreicht?: " + datum_zeit)
        break
    
    except:
        raise
    
    finally:
        bayern3.set_letzte_url(url)
        db.commit()

db.close()


