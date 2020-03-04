#!/usr/bin/zsh

scanimage --format=png --batch=lieferschein%d.png --progress --resolution 300 -x 210 -y 297
# python3 ~/bin/delivery-note-sort.py
