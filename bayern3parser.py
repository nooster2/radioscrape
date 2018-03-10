from bs4 import BeautifulSoup
import sqlite3
import urllib.request as urllib2

# Connection zur Datenbank
connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()

# zuletzt geparste URL als Startpunkt zum weitermachen
url = cursor.execute("select url from letztesParsen where id = 1").fetchone()[0]

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
            try:
                cursor.execute("""insert into bayern3(datum_zeit, interpret, titel)
                                  values(?, ?, ?);""", (datum_zeit, interpret, titel))
            except sqlite3.IntegrityError:
                print("Datenbank Unique verletzt: " + datum_zeit)

        # nächste URL
        url = 'http://www.br.de' + soup.find('p', 'playlist_navi_down').a.get('href')

    except AttributeError: # wird ausgelöst, wenn keine "nächste URL" gefunden werden kann
        print("AttributeError. Vermutlich letzte Seite erreicht: " + datum_zeit)
        break
    
    except:
        print("Unerwarteter Fehler")
        raise
    
    finally:
        cursor.execute("update letztesParsen set url = '" + url + "' where id = 1")
        connection.commit()


connection.close()


