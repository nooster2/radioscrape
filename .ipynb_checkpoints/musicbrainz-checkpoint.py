import sqlite3
import musicbrainzngs
# zum Initialisieren der API
musicbrainzngs.set_useragent("radioscrape", "0.1", contact=None)
# Doku: https://python-musicbrainzngs.readthedocs.io/en/v0.6/api/
# Wir brauchen das Modul von Musicbrainzngs:
# pip install musicbrainzngs




# Datenbankoperationen
connection = sqlite3.connect('db.sqlite3')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
sql = "SELECT * FROM bayern3"
bayern3 = cursor.execute(sql).fetchall()
for eintrag in bayern3[10000:]:
    try:
        # Jetzt wird geschaut, welche Daten MB für uns zu diesem Song parat hält
        result = musicbrainzngs.search_releases(artist=eintrag['interpret'], release=eintrag['titel'])
        release=result['release-list'][0]
        #print(release)
    
        # MB liefert ein dict zurück, das ich jetzt außeinanderpflüge und sortiere
        mb_score = int(release['ext:score'])	
        mb_id = release['id']
        mb_interpret = release['artist-credit'][0]['artist']['name']
        mb_titel = release['title']
        mb_jahr = release['date']
        #plattenlabel=release['label-info-list'][0]['label']['name']
        mb_land = release['release-event-list'][0]['area']['name']    

        print('Score: ', mb_score)
        print('ID: ', mb_id)
        print('Interpret: ', mb_interpret)
        print('Titel: ', mb_titel)
        print('Jahr: ', mb_jahr)
        #print('Label: ', plattenlabel)
        print('Land: ', mb_land)
        print('')
    
    except KeyError:
        print(eintrag['datum_zeit'], ' ', eintrag['interpret'], ' ', eintrag['titel'], ': Fehler beim Lesen aus musicbrainz.')
        raise
        
#for release in result['release-list']:

    
# Wenn die Übereinstimmung der Metadaten kleiner als 80% ist, soll der Titel zum
# debuggen ausgegeben werden.
#if richtigkeit < 80:	

#print(u"{id1}: {id2} - {id3} ({id4})".format(id1=mbid, id2=saenger, id3=titel, id4=jahr))
#else:
#    print("check: ", saenger, ' - ', titel, ' (',jahr,')')


# Jetzt müssen die Daten noch in die DB geschrieben werden, fertig :)		
		
connection.close()
