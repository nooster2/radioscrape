# import sqlite3
import musicbrainzngs

# zum Initialisieren der API
musicbrainzngs.set_useragent("radioscrape", "0.1", contact=None)
# Doku: https://python-musicbrainzngs.readthedocs.io/en/v0.6/api/

# Wir brauchen das Modul von Musicbrainzngs:
# pip install musicbrainzngs

# Für später: Datenbankoperationen
# connection = sqlite3.connect('datenbank.db')
# cursor = connection.cursor()
# connection.close()

# Schritt 1: Verbindung zur musicbrainz aufbauen und ID des Künstlers herausfinden
# Beispiel: 
interpretdb ="Sigrid"
songdb = "Strangers"

result = musicbrainzngs.search_releases(artist=interpretdb, release=songdb)
release=result['release-list'][0]
#print(release)

#for release in result['release-list']:
richtigkeit = int(release['ext:score'])
if richtigkeit > 80:
	mbid=release['id']
	saenger=release['artist-credit'][0]['artist']['name']
	titel=release['title']
	jahr=release['date']
	plattenlabel=release['label-info-list'][0]['label']['name']
	land=release['release-event-list'][0]['area']['name']
	
	
	print('ID: ', mbid)
	print('Interpret: ',saenger)
	print('Titel: ', titel)
	print('Jahr: ', jahr)
	print('Label: ', plattenlabel)
	print('Land: ', land)
	#print(u"{id1}: {id2} - {id3} ({id4})".format(id1=mbid, id2=saenger, id3=titel, id4=jahr))

		
		
		# Schritt 2: ID des Songs herausfinden

# Schritt 3: vom Song folgendes in die DB notieren: Veröffentlichungsdatum, Label