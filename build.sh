#!/bin/bash

# Compile UI
pyuic4 ./points2one/frmPoints2One.ui -o ./points2one/ui_frmPoints2One.py

# Update translation files
pylupdate4 ./points2one/*.py -ts \
./points2one/i18n/points2one_es_ES.ts \
./points2one/i18n/points2one_ru_RU.ts \
./points2one/i18n/points2one_fr_FR.ts

# Release translation files
lrelease ./points2one/i18n/*.ts
