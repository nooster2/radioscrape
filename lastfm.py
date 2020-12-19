import urllib.request, json, db
import re # damit werden Klammern aus dem Titel entfernt, z.B. I see fire (Single remix)

#Application name 	radioscrape
API_key = "868e30a436547b8fb8b40fe5b4a4d9d4"
#Shared secret 	dd73c3fda30d78a97fc09ce09dae0b7d
#Registered to 	Nooster


# Connection zur Datenbank
db.connect()
songs = db.songs()


for eintrag in songs.lfladen():
    try:
        interpret = eintrag['interpret']
        titel = eintrag['titel']
        titel = re.sub(r'\([^)]*\)', '', titel) # entfernt Klammer aus dem Titel https://im-coder.com/wie-kann-ich-text-in-klammern-mit-einem-regex-entfernen.html 
        titel = re.sub(r'\[[^)]*\]', '', titel)
        url='http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key='+API_key+'&artist='+interpret+'&track='+titel+'&format=json'
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
                print("OK: "+interpret+ " - "+titel+": "+mbid)
            else:
                print(" X Not Found: "+interpret+ " - "+titel)
    except KeyboardInterrupt:
        print("Abort from user")
        break
    except:
        print(" X Something went wrong :( Song #"+str(eintrag['id']))
db.close()   
##http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=868e30a436547b8fb8b40fe5b4a4d9d4&artist=cher&track=believe&format=json