# Airport Service API
API service for ordering tickets to airport. Written on DRF

# The content
- [Features](#features)
- [Installing with GitHub](#installing-with-github)
- [Run on docker](#run-on-docker)
- [Get access](#get-access)

## Features

- **JWT authentication**
- **Admin panel (/admin/)**
- **Documentation (/api/doc/swagger/)**
- **Ability for authorized user creat orders with tickets**
- **Filtering Flights and Routes**

## Installing with GitHub
Install PostgresSQL and create your db
```
git clone https://github.com/HlovaOleh/airport-service.git  
cd airport-service  
python -m venv venv  
venv\Scripts\activate # (For Windows)
source venv/bin/activate # (For Linux/Mac)
pip install -r requirements.txt
set DB_HOST="your db hostname"
set DB_NAME="your db name"
set DB_USER="your db username"
set DB_PASSWORD="your db password"
set SECRET_KEY="your secret key"
python manage.py migrate
python manage.py runserver
```
don't forget to copy .env.sample to .env and fill out it with your info 

## Run on docker
Docker should be installed and run
```
docker-compose build
docker-compose up
```

## Get access

- create user via /api/user/register/
- get access token via /api/user/token/