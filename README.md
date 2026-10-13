

# Property Management System


## Instructions to run it on localhost

Step 1:
clone the github repository
```
git clone <repo>
```
cd into the project


Step 2:
Create python virtual environment and activate
```
python3 -m venv .venv
source .venv/bin/activate
```
Step 3:
Install dependencies
```
pip install -r requirements.txt
```
Step 4:
Run a postgresql DB locally
```
# sudo -u postgres psql on Linux,
# psql -U postgres on macOS
CREATE DATABASE propertydb;
CREATE USER propertyuser WITH PASSWORD 'propertypass';
ALTER DATABASE propertydb OWNER TO propertyuser;
```

Step 5:
Configure environment variables

Create a .env file from the example configuration:
```
cp .env.example .env
```
Ensure the database configuration in .env matches the PostgreSQL database and user created in Step 4.

Also ensure that required settings, such as SECRET_KEY and database connection details, are configured according to the project's settings.


Step 6:
Run migrate and runserver
```
python3 manage.py migrate
python3 manage.py runserver
```

Access the backend at baseurl = http://localhost:8000


API Documentation

A Postman collection containing the API requests is provided in the repository:

Hmlet.postman_collection.json

Import this file into Postman to explore and test the available endpoints.


