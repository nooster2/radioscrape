import sqlite3

conn_alt = sqlite3.connect('datenbank.db')
cursor_alt = conn_alt.cursor()

conn_neu = sqlite3.connect('db.sqlite3')
cursor_neu = conn_neu.cursor()

bayern3 = cursor_alt.execute('SELECT * FROM bayern3').fetchall()
for eintrag in bayern3:
    cursor_neu.execute("""
        INSERT INTO bayern3 (datum_zeit, interpret, titel)
        VALUES (?,?,?);
    """, eintrag)

letztesParsen = cursor_alt.execute('SELECT url FROM letzte_url').fetchall()
for eintrag in letztesParsen:
    cursor_neu.execute("""
        INSERT INTO letztesParsen (url)
        VALUES (?);
    """, eintrag)


conn_neu.commit()

conn_neu.close()
conn_alt.close()

