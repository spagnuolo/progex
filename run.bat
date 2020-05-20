@echo off

set FLASK_APP=src
set FLASK_ENV=development

python -m venv venv
src\venv\Scripts\activate.bat & flask run