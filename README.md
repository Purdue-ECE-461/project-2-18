# project-2-18

https://project-group18.uc.r.appspot.com/

## What this does
endpoints
/packages -> shows all packages in database

/package -> shows POST packageCreate database

/package/byName/{name} -> shows GET, PUT, DELETE functions for repository

/package/{id} -> shows GET, PUT, DELETE functions for repository

/package/{id}/rate -> shows GET functions for repository rate

login button on top right corner of every page -> authentication

username = ece461defaultadminuser

password = correcthorsebatterystaple123(!__+@**(A

## Usage
In order to run on local host

pip install all requirements shown in requirements.txt

run the following commands

python3 manage.py makemigrations p18website

python3 manage.py migrate

python3 manage.py runserver

click the link on the command line

http://127.0.0.1:8000/

