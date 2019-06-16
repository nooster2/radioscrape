import time
import datetime
import sqlite3
import pandas as pd
import matplotlib as plt
import numpy as np
import seaborn as sns  # für das Styling der Ausgabe https://pandas.pydata.org/pandas-docs/stable/style.html#Builtin-Styles


# Ziel: Wie viele Songs wurden am Tag gespielt. Am besten für das ganze Jahr

# Erstmal das heutige Datum feststellen
end_date = datetime.date.today()
start_date = datetime.date(2019, 1, 1)

# Quelle: https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python 
def daterange(start_date, end_date): 
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


# Daten aus Datenbank laden
connection = sqlite3.connect('./db.sqlite3')
df = pd.read_sql_query("""SELECT bayern3.id, datum_zeit, interpret, titel, label FROM bayern3 
                        INNER JOIN songs ON bayern3.song=songs.id""", connection, index_col='id')
connection.close()

# Spalte mit nur dem Datum hinzufügen
df['datum'] = pd.to_datetime(df['datum_zeit']).dt.date
# Separaten DataFrame für den Vergleich
vergleich = pd.DataFrame()
# Eine Spalte je Kalenderwoche, titel als Index
for single_date in daterange(start_date, end_date):
    vergleich[single_date] = df[df['datum'] == single_date].count()
    
# Alle Zeilen droppen, die NaN enthalten (liegt vor, wenn der Titel in einer Woche nicht gespielt wurde)
#vergleich = vergleich.dropna(how='any')
### Schöne Matrix füllen
ergebnis = np.zeros([31,12])
for monat in range(1,13):
    for tag in range(1,32):
        try: 
            ergebnis[tag-1][monat-1] = vergleich[datetime.date(2019,monat,tag)]['datum_zeit']
        except:
            pass
            
# Erstelle einen Dataframe daraus:
ergebnisdf = pd.DataFrame(data=ergebnis, index=range(1,32), columns=range(1,13))


# Seaborn Bedingte Formatierung
cm = sns.light_palette("green", as_cmap=True)
ergebnisbild = ergebnisdf.style.background_gradient(cmap=cm)

# Seaborn Heatmap
# https://seaborn.pydata.org/generated/seaborn.heatmap.html
# https://matplotlib.org/users/colormaps.html
plt.pyplot.figure(figsize=(10, 16))
heatmap = sns.heatmap(ergebnisdf, annot=True, fmt="g", cbar=False, cmap="RdYlGn")

# Heatmap exportieren
savename = './Auswertung/img/out_'+str(end_date)+'.png'
fig = heatmap.get_figure()
fig.savefig(savename) 