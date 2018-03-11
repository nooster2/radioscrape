import sqlite3

connection = sqlite3.connect('../db.sqlite3')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE bayern3 (
        id INTEGER,
        datum_zeit TEXT,
        song INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(song) REFERENCES songs(id),
        UNIQUE (datum_zeit, song)
    );
""")

cursor.execute("""
    CREATE TABLE songs (
        id INTEGER,
        interpret TEXT,
        titel TEXT,
        veroeffentlichung TEXT,
        label TEXT,
        PRIMARY KEY (id),
        UNIQUE (interpret, titel)
        );
    """)

cursor.execute("""
    CREATE TABLE letztesParsen (
        id INTEGER,
        sender TEXT,
        url TEXT,
        PRIMARY KEY (id)
        );
    """)

connection.commit()
connection.close()

