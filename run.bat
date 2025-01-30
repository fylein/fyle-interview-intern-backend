@echo off

:: Setting flask environment
set FLASK_APP=core/server.py

:: Run required migrations
:: flask --app core/server.py db init -d core/migrations/
:: flask --app core/server.py db migrate -m "Initial migration." -d core/migrations/
:: flask --app core/server.py db upgrade -d core/migrations/

:: Run server
hupper -m waitress --port=7755 core.server:app
