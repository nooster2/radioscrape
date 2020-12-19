import sqlite3

# Connection zur alten Datenbank
conn_alt = sqlite3.connect('../db_alt.sqlite3')
conn_alt.row_factory = sqlite3.Row
cursor_alt = conn_alt.cursor()

# Connection zur neuen Datenbank
conn_neu = sqlite3.connect('../db.sqlite3')
conn_neu.row_factory = sqlite3.Row
cursor_neu = conn_neu.cursor()

# Daten aus alter Datenbank laden und in neue schreiben
bayern3 = cursor_alt.execute('SELECT * FROM bayern3').fetchall()
for eintrag in bayern3:
    try:
        cursor_neu.execute("""
            INSERT INTO songs (interpret, titel)
            VALUES (?,?);
            """, (eintrag['interpret'], eintrag['titel']))
    
    except sqlite3.IntegrityError: # Wenn der Titel schon in songs enthalten ist
        pass

    try:
        song = cursor_neu.execute("""SELECT id FROM songs WHERE interpret = ? AND titel = ?;""", (eintrag['interpret'], eintrag['titel'])).fetchone()
        cursor_neu.execute("""
            INSERT INTO bayern3 (datum_zeit, song)
            VALUES (?,?);
            """, (eintrag['datum_zeit'], song[0]))
    
    except TypeError: # Nötig, da teilweise der Interpret leer ist und stattdessen beim Titel mit dabei steht
        print(eintrag['datum_zeit'], ' ', eintrag['interpret'], ' ', eintrag['titel'])
        song = cursor_neu.execute("""SELECT id FROM songs WHERE titel = ?;""", (eintrag['titel'],)).fetchone()
        cursor_neu.execute("""
            INSERT INTO bayern3 (datum_zeit, song)
            VALUES (?,?);
            """, (eintrag['datum_zeit'], song[0]))
    
letztesParsen = cursor_alt.execute('SELECT url FROM letztesParsen').fetchall()
for eintrag in letztesParsen:
    cursor_neu.execute("""
        INSERT INTO letztesParsen (url)
        VALUES (?);
        """, eintrag)


conn_neu.commit()

conn_neu.close()
conn_alt.close()

