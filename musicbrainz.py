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
        print()
        result = musicbrainzngs.search_releases(artist=eintrag['interpret'], release=eintrag['titel'])
        if bool(result['release-list']): # Manchmal ist ein Ergebnis-dict leer, siehe z.B. Interpret: Fibel, Titel: Paynesgrau
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

            if mb_score < 80:
                print('Score: ', mb_score, '    <--!!!!!!!')
            else:
                print('Score: ', mb_score)
            print('ID: ', mb_id)
            print('Interpret: ', mb_interpret)
            print('Titel: ', mb_titel)
            print('Jahr: ', mb_jahr)
            print('Label: ', mb_label)
            print('Land: ', mb_land)
            print('')
            
            # Jetzt müssen die Daten noch in die DB geschrieben werden, fertig :)
            # song_id, veroeffentlichung, label, land, musicid, musicbrainzscore	
           # try:
            #songs.schreibemusicbrainz((id, str(mb_jahr), str(mb_label), str(mb_land), str(mb_id), mb_score))
            songs.schreibemusicbrainz((mb_id, mb_label, mb_land, mb_jahr, mb_score, eintrag['id']))
            db.commit()
            print("In DB eingetragen!")
            # except:
                # print("Eintragen fehlgeschlagen!")
        
    except KeyError:
        print('!!!!!!!!!!!!!!!!!!!!!')
        print(eintrag['interpret'], ' ', eintrag['titel'], ': Fehler beim Lesen aus musicbrainz.')
        print('!!!!!!!!!!!!!!!!!!!!!')
        print
        with open('errormusicbrainz.log', 'a') as f:
            logeintrag = '{"interpret" : "' + str(eintrag['interpret']) + '", "titel" : "' + str(eintrag['titel']) + '", "song-id" : "'+ str(eintrag['id']) + '"}, \n'
            f.write(logeintrag)
            f.close()

    except UnicodeEncodeError:
        print('Unicode is a bitch :(')

	
db.close()
