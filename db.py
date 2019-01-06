import sqlite3

# Conn als globale Variable instanzieren
conn = None

# Connection zur Datenbank
def connect():
    global conn 
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row

def commit():
    conn.commit()

def close():
    conn.close()

class bayern3:
    def __init__(self):
        self.cursor = conn.cursor()
    
    def eintragen(self, datum_zeit, interpret, titel):
        song_id = self.cursor.execute("""
            SELECT id FROM songs
            WHERE interpret = ? AND titel = ?;
            """, (interpret, titel)).fetchone()
        
        
        if song_id is None: # Wenn die Interpret-Titel-Kombination noch nicht vorhanden ist
            self.cursor.execute("""
                INSERT INTO songs (interpret, titel)
                VALUES (?, ?);
                """, (interpret, titel))
            
            song_id = self.cursor.execute("""
                SELECT id FROM songs
            WHERE interpret = ? AND titel = ?;
            """, (interpret, titel)).fetchone()
            
    
        try:
            self.cursor.execute("""
                INSERT INTO bayern3 (datum_zeit, song)
                VALUES (?, ?);
                """, (datum_zeit, song_id[0]))
        
        except sqlite3.IntegrityError: # Tritt auf, da die letzte URL vom letzten Mal Parsen nochmal abgearbeitet wird
            print('Schon in DB: ' + datum_zeit)
    
    def get_letzte_url(self):
        return self.cursor.execute("SELECT url FROM letztesParsen WHERE id = 1").fetchone()[0]
    
    def set_letzte_url(self, url):
        self.cursor.execute("UPDATE letztesParsen SET url = '" + url + "' WHERE id = 1")

class songs:
    def __init__(self):
        self.cursor = conn.cursor()
    
    def laden(self):
        return self.cursor.execute("""SELECT * FROM songs
            WHERE musicid IS NULL;""").fetchall()
    def lfladen(self):
        return self.cursor.execute("""SELECT * FROM songs
            WHERE lfmbid IS NULL;""").fetchall()
            
    def schreibemusicbrainz(self, task):
        sql ="""UPDATE songs
        SET musicid = ?,
            label = ?,
            land = ?,
            veroeffentlichung = ?,
            musicbrainzscore = ?
        WHERE id = ?"""
        return self.cursor.execute(sql,task)
        
    def AddLastFmToTable(self):
        sql="alter table songs add column lfland text"
        return self.cursor.execute(sql)
        
    def schreibelastfm(self, task):
        sql ="""UPDATE songs
        SET lfmbid = ?,
            lfinterpret = ?,
            lftitel = ?,
            lfveroeffentlichung = ?,
            lflabel = ?,
            lfland = ?
        WHERE id = ?"""
        return self.cursor.execute(sql,task)