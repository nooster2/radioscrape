import musicbrainzngs
import db
# zum Initialisieren der API
musicbrainzngs.set_useragent("radioscrape", "0.1", contact=None)
# Doku: https://python-musicbrainzngs.readthedocs.io/en/v0.6/api/
# Wir brauchen das Modul von Musicbrainzngs:
# pip install musicbrainzngs


# Connection zur Datenbank
db.connect()
songs = db.songs()

for eintrag in songs.laden():
    try:
        # Jetzt wird geschaut, welche Daten MB für uns zu diesem Song parat hält
        result = musicbrainzngs.search_releases(artist=eintrag['interpret'], release=eintrag['titel'])
        
        # Überprüfen, ob mehrere Einträge in der Ergebnisliste den Score von 100 haben
        scoreCheck = []
        for i in range(0,5): # die ersten 5 Ergebnisse werden angeschaut
            score = int(result['release-list'][i]['ext:score'])
            if score == 100:
                scoreCheck.append(score)
                        
        listeDerVolltreffer = len(scoreCheck)       # So viele Ergebnisse der Suche haben einen Score von 100
        # Wenn es mehr als einen 100% Treffer gibt, wird das in die Datei needsmainenancemb.log geschrieben
        if listeDerVolltreffer == 0:
            print('Kein Suchergebnis')
            with open('needsmainenancemb.log', 'a') as f:
                logeintrag = '{"song-id" : "' + str(eintrag['id']) + '", "titel" : "' + str(eintrag['titel']) + '", "interpret" : "'+ str(eintrag['interpret']) + '", "reason" : "tooless", "count" : "0" }, \n'
                f.write(logeintrag)
                f.close()
        if listeDerVolltreffer > 1:
            print('Mehrfachtreffer! Insgesamt ' + str(listeDerVolltreffer))
            with open('needsmainenancemb.log', 'a') as f:
                logeintrag = '{"song-id" : "' + str(eintrag['id']) + '", "titel" : "' + str(eintrag['titel']) + '", "interpret" : "'+ str(eintrag['interpret']) + '", "reason" : "toomany", "count" : "' + str(listeDerVolltreffer) + '" }, \n'
                f.write(logeintrag)
                f.close()
            
        else: # Wenn es nur einen Eintrag mit Score 100 gibt, kann der Eintrag erfolgen! 
            print('Nur ein Volltreffer')
            release=result['release-list'][0]
            #print(release)
            
            #for release in result['release-list']:
            
            # MB liefert ein dict zurück, das ich jetzt außeinanderpflüge und sortiere
            mb_score = int(release['ext:score'])
            mb_id = release['id']
            mb_interpret = release['artist-credit'][0]['artist']['name']
            mb_titel = release['title']
            mb_jahr = release['date']
            #
            try:
                mb_label=release['label-info-list'][0]['label']['name']
            except:
                mb_label="NaN"
            mb_land = release['release-event-list'][0]['area']['name']    

            # print('ID: ', mb_id)
            # print('Interpret: ', mb_interpret)
            # print('Titel: ', mb_titel)
            # print('Jahr: ', mb_jahr)
            # print('Label: ', mb_label)
            # print('Land: ', mb_land)
            # print('')
            
            # Jetzt müssen die Daten noch in die DB geschrieben werden, fertig :)
            songs.schreibemusicbrainz((mb_id, mb_label, mb_land, mb_jahr, mb_score, eintrag['id']))
            print("In DB eingetragen:" + str(eintrag['id']) + ': ' + mb_interpret + ' - ' + mb_titel)
        
    except KeyError:
        print('!!!!!!!!!!!!!!!!!!!!!')
        print(eintrag['interpret'], ' ', eintrag['titel'], ': Fehler beim Lesen aus musicbrainz.')
        print('!!!!!!!!!!!!!!!!!!!!!')
        with open('errormusicbrainz.log', 'a') as f:
            logeintrag = '{"interpret" : "' + str(eintrag['interpret']) + '", "titel" : "' + str(eintrag['titel']) + '", "song-id" : "'+ str(eintrag['id']) + '"}, \n'
            f.write(logeintrag)
            f.close()

    # except UnicodeEncodeError:
        # print('Unicode is a bitch :(')

db.commit()	
db.close()
