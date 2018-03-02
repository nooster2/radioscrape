import sqlite3
import musicbrainzngs
# zum Initialisieren der API
musicbrainzngs.set_useragent("radioscrape", "0.1", contact=None)
# Doku: https://python-musicbrainzngs.readthedocs.io/en/v0.6/api/
# Wir brauchen das Modul von Musicbrainzngs:
# pip install musicbrainzngs




# Datenbankoperationen
connection = sqlite3.connect('datenbank.db')
cursor = connection.cursor()
sql = "SELECT * FROM bayern3"
interpreten = cursor.execute(sql).fetchall()
for r in interpreten[0:100]:
	try:
		# Dieser Song ist in der Datenbank hinterlegt und sollte um Daten ergänzt werden: 
		interpretdb =r[1]
		songdb = r[2]
		
		# Jetzt wird geschaut, welche Daten MB für uns zu diesem Song parat hält
		result = musicbrainzngs.search_releases(artist=interpretdb, release=songdb)
		release=result['release-list'][0]
		#print(release)

		#for release in result['release-list']:
		
		# MB liefert ein dict zurück, das ich jetzt außeinanderpflüge und sortiere
		richtigkeit = int(release['ext:score'])	
		mbid=release['id']
		saenger=release['artist-credit'][0]['artist']['name']
		titel=release['title']
		jahr=release['date']
		#plattenlabel=release['label-info-list'][0]['label']['name']
		land=release['release-event-list'][0]['area']['name']
		
		# Wenn die Übereinstimmung der Metadaten kleiner als 80% ist, soll der Titel zum
		# debuggen ausgegeben werden.
		if richtigkeit < 80:	
			print('Score: ', richtigkeit)
			print('ID: ', mbid)
			print('Interpret: ', saenger)
			print('Titel: ', titel)
			print('Jahr: ', jahr)
			#print('Label: ', plattenlabel)
			print('Land: ', land)
			print('')
			#print(u"{id1}: {id2} - {id3} ({id4})".format(id1=mbid, id2=saenger, id3=titel, id4=jahr))
		else:
			print("check: ", saenger, ' - ', titel, ' (',jahr,')')
	except UnicodeEncodeError:
		print('Unicode is a bitch :(')
	except:
		print("Unerwarteter Fehler")

# Jetzt müssen die Daten noch in die DB geschrieben werden, fertig :)		
		
connection.close()
