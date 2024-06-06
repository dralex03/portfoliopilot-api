# PortfolioPilot API

## Requirements
  * Python 3.12 (minimum)

## Configuration of .env File
  * Create a .env File in the root project directory

### Database Settings
  * Add the variable:
```
DATABASE_URL = postgresql+psycopg2://username:password@host:port/database_name
```
  * Replace the username, password, host, port and database_name placeholders with your actual database credentials

  * If you are running the database tests locally, make sure that the ```DATABASE_URL``` for the production database is replaced with the
    one for the test database
### Flask Settings
  * Settings for dev environment:
```
FLASK_APP=src
FLASK_DEBUG=1
```
  * Settings for production environment:
```
// TODO
```

### JWT / Auth Settings
  * JWT Authentication requires a secret key:
```
JWT_SECRET_KEY=super_secret_key
```

### Conclusion .env File Example
```
# PostgreSQL Database
DATABASE_URL = postgresql+psycopg2://postgres:1234@localhost:5432/PortfolioPilotDB

# Flask
FLASK_APP=src
FLASK_DEBUG=1

# JWT Auth
JWT_SECRET_KEY=super_secret_key
```

## Start the API application
  * Run the following command on repository level to start the application: `python . run`
