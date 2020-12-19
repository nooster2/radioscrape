#!/bin/sh
cd ./python/radioscrape
git checkout master
python3 bayern3parser.py
python3 ./Auswertung/tageweise.py
git add .
git commit -am "autostart: Daten geparst"
git push
echo Press Enter...
read
