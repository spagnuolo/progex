### minimalistisch und flexibel mit wenig Abhänigkeiten

- Frontend/GUI: Plain HTML/CSS
  - kein Lust mich mit einem JS/Framework rumzuschlagen
- Backend: Flask/Python 3.x
  - einfach zu lernen und der Focus bleibt auf Python
- Database: sqlite
  - in Python enthalten

ANLEITUNG ZUM STARTEN DES SERVERS:
IM SRC FOLDER:

    1. python3 -m venv venv
    2. windows: venv\Scripts\activate.bat
        linux: venv/bin/activate

    3. pip install -r requirements.txt
    4. cd ..
    5.windows:
        set FLASK_APP=src
        set FLASK_ENV=development

    5.linux:
        export FLASK_APP=src
        export FLASK_ENV=development

    6. python3 -m flask run

        ODER
        flask run

if you add new pip module run
pip freeze > requirements.txt

<!-- pip3 install flask flask-sqlalchemy flask_login
python3 -m pip install flask
python3 -m pip install flask-sqlalchemy 4.
python3 -m pip install flask_login -->
