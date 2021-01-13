import sqlite3

connection = sqlite3.connect('../db.sqlite3')
cursor = connection.cursor()

    
cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER,
        interpret TEXT,
        titel TEXT,
        veroeffentlichung TEXT,
        label TEXT,
        PRIMARY KEY (id),
        UNIQUE (interpret, titel)
        );
    """)
    
cursor.execute("""alter table songs add column musicid text""")
#, musicid TEXT, musicbrainzscore INTEGER
connection.commit()
connection.close()