import sqlite3
import musicbrainzngs
import db
# zum Initialisieren der API
musicbrainzngs.set_useragent("radioscrape", "0.1", contact=None)

db.connect()
songs = db.songs()
bayern3 = db.bayern3()
id = [5,6,16,18,19,20,23,34,37,40,41,42,47,56,57,58,64,67,70]

for i in id:
    eintrag = songs.ladeeinzelsong(str(i))
    try:
            # Jetzt wird geschaut, welche Daten MB für uns zu diesem Song parat hält
        result = musicbrainzngs.search_releases(artist=eintrag['interpret'], release=eintrag['titel'])
        vorkommnisse = bayern3.zaehlevorkommen(str(i))
        print(vorkommnisse)
        # Überprüfen, ob mehrere Einträge in der Ergebnisliste den Score von 100 haben
        scoreCheck = []
        for j in range(0,5): # die ersten 5 Ergebnisse werden angeschaut
            score = int(result['release-list'][j]['ext:score'])
            if score == 100:
                scoreCheck.append(score)
                        
        listeDerVolltreffer = len(scoreCheck)       # So viele Ergebnisse der Suche haben einen Score von 100
        print(listeDerVolltreffer)
        for k in range(0,listeDerVolltreffer):
            release=result['release-list'][k]
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
            print(mb_interpret + ' - ' + mb_titel + ' Label: ' + mb_label + ' Jahr: ' + mb_jahr + ' Land: ' + mb_land)
            # Jetzt müssen die Daten noch in die DB geschrieben werden, fertig :)
            # songs.schreibemusicbrainz((mb_id, mb_label, mb_land, mb_jahr, mb_score, eintrag['id']))
            with open('songmaintainence.csv', 'a') as f:
                logeintrag = '0; '+ str(i) + '; '+ str(vorkommnisse) + '; '+ str(eintrag['interpret']) + '; '+ str(eintrag['titel']) + '; '+ str(mb_interpret) + '; '+ str(mb_titel) + '; '+ str(mb_jahr) + '; '+ str(mb_label) + '; '+ str(mb_land) + '; '+ str(mb_id) + '; \n'
                f.write(logeintrag)
                f.close()   
    except:
        print('Fehlgeschlagen!')

db.commit()
db.close()