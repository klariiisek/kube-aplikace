#!/bin/sh

# Počkáme na start PostgreSQL
sleep 5

# Provedeme migrace
flask db upgrade

# Spustíme aplikaci s vyšším timeoutem a 2 workery
exec gunicorn --bind 0.0.0.0:5001 --workers 2 --timeout 60 --log-level info app:app
