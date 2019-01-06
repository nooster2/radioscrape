import urllib.request, json, db

#Application name 	radioscrape
API_key = "868e30a436547b8fb8b40fe5b4a4d9d4"
#Shared secret 	dd73c3fda30d78a97fc09ce09dae0b7d
#Registered to 	Nooster


# Connection zur Datenbank
db.connect()
songs = db.songs()


for eintrag in songs.lfladen():
    try:
        url='http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key='+API_key+'&artist='+eintrag['interpret']+'&track='+eintrag['titel']+'&format=json'
        with urllib.request.urlopen(url) as urljson:
            data = json.loads(urljson.read().decode())
            try:
                mbid=data['track']['mbid']
            except:
                mbid="NaN"
            try:
                artist=data['track']['artist']['name']
            except:
                artist="NaN"
            try:
                track=data['track']['name']
            except:
                track="NaN"
                
            if mbid != "NaN":
                songs.schreibelastfm((mbid, artist, track, "NaN", "NaN", "NaN", eintrag['id']))
                db.commit()
                print("In DB eingetragen!")
            print("ID: "+mbid)
            print("Ar: "+artist+ " ("+eintrag['interpret']+")")
            print("Tr: "+track+ " ("+eintrag['titel']+")")
            print()
    except KeyboardInterrupt:
        print("Abort from user")
        break
    except:
        print("Something went wrong :(")
db.close()   
##http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=868e30a436547b8fb8b40fe5b4a4d9d4&artist=cher&track=believe&format=json