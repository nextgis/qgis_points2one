#!/bin/bash

# Update translation files
pylupdate5 ./points2one/*.py -ts \
./points2one/i18n/points2one_es_ES.ts \
./points2one/i18n/points2one_ru_RU.ts \
./points2one/i18n/points2one_fr_FR.ts

# Release translation files
lrelease ./points2one/i18n/*.ts
