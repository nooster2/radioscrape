import sqlite3

connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE bayern3 (
        id INTEGER,
        datum_zeit TEXT,
        interpret TEXT,
        titel TEXT,
        PRIMARY KEY (id),
        UNIQUE (datum_zeit, interpret, titel)
    );
""")

cursor.execute("""
    CREATE TABLE letztesParsen (
        id INTEGER,
        url TEXT,
        PRIMARY KEY (id)
    );
""")

connection.commit()
connection.close()

