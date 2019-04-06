#!/bin/sh
cd /c/Users/HP/Documents/git-Projekte/radioscrape
git checkout master
python bayern3parser.py
git add .
git commit -am "autostart: Daten geparst"
git push
echo Press Enter...
read