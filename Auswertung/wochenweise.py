import time
import datetime
import sqlite3
import pandas as pd
import matplotlib as plt

# Erstmal das heutige Datum feststellen
today = datetime.datetime.today()
print(today)
weeknr = today.isocalendar()[1]
print(weeknr)

# Daten aus Datenbank laden
connection = sqlite3.connect('../db.sqlite3')
df = pd.read_sql_query("""SELECT bayern3.id, datum_zeit, interpret, titel FROM bayern3 
                        INNER JOIN songs ON bayern3.song=songs.id""", connection, index_col='id')
connection.close()

# Spalte mit der Kalenderwoche hinzufügen
df['woche'] = pd.to_datetime(df['datum_zeit']).dt.week

# Separaten DataFrame für den Vergleich
vergleich = pd.DataFrame()
# Eine Spalte je Kalenderwoche, titel als Index
for i in range(weeknr-5, weeknr+1):
    vergleich['KW'+str(i)] = df[df['woche'] == i].groupby('titel').count().sort_values(by='datum_zeit', ascending=False)['datum_zeit']
# Alle Zeilen droppen, die NaN enthalten (liegt vor, wenn der Titel in einer Woche nicht gespielt wurde)
vergleich = vergleich.dropna(how='any')
# Alternativ mit 0 ersetzen
# vergleich = vergleich.fillna(value=0)



# Ausgabe der Ergebnisse als Tabelle:
# vergleich.head(10)


# Ausgabe der Ergebnisse als Grafik
vergleich.T.iloc[:,0:10].plot()
plt.pyplot.grid(True)