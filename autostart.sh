#!/bin/sh
cd /c/Users/HP/Documents/git-Projekte/radioscrape
git checkout master
/c/Users/HP/Anaconda3/python.exe bayern3parser.py
/c/Users/HP/Anaconda3/python.exe ./Auswertung/tageweise.py
git add .
git commit -am "autostart: Daten geparst"
git push
echo Press Enter...
read