from bs4 import BeautifulSoup
import sqlite3
import urllib.request as urllib2

connection = sqlite3.connect('datenbank.db')
cursor = connection.cursor()

url = cursor.execute("select url from letzte_url where id = 1").fetchone()[0]

while True:
    try:
        html_page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html_page, 'html.parser')

        datum = url.split('_date-')[1].split('_hour-')[0]
        zeiten = soup.find('dl', 'music_research').find_all('dt', 'time')
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
        
        url = 'http://www.br.de' + soup.find('p', 'playlist_navi_down').a.get('href')

    except AttributeError:
        print("AttributeError. Vermutlich letzte Seite erreicht: " + datum_zeit)
        break
    
    except:
        print("Unerwarteter Fehler")
        break
    
    finally:
        cursor.execute("update letzte_url set url = '" + url + "' where id = 1")
        connection.commit()


connection.close()


