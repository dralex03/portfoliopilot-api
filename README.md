# PortfolioPilot API

## Requirements
  * Python 3.12 (minimum)
  * PostgreSQL Database (local or remote)

## Installation

First of all make sure, that you have installed the [required tools](#Requirements).

### Clone Repository

Clone the Repository:

``git clone https://github.com/dralex03/portfoliopilot-api.git``

Change  Directory:

``cd portfoliopilot-api``

---

### Installation of python packages

Create a virtual environment (optional but recommended)

``python -m venv venv``

Activate the virtual environment:

On Windows:
``venv\Scripts\activate``

On macOS and Linux:
``source venv/bin/activate``

Install the required packages:
``pip install -r requirements.txt``

---

### Configuration of .env File
  * Create a .env File in the root project directory

#### Database Settings
  * Add the variable:
```
DATABASE_URL = postgresql+psycopg2://username:password@host:port/database_name
```
  * Replace the username, password, host, port and database_name placeholders with your actual database credentials

  * If you are running the database tests locally, make sure that the `DATABASE_URL` is set to `sqlite:///:memory:`
#### Flask Settings
  * Settings for dev environment:
```
FLASK_APP=src
FLASK_DEBUG=1
```
  * Settings for production environment:
```
// TODO
```

#### JWT / Auth Settings
  * JWT Authentication requires a secret key:
```
JWT_SECRET_KEY=replace_this_super_secret_key
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

---

## Start the API application
  * Run the following command on repository level to start the application: `python . run` or `flask run`
  * To see all available API endpoints, run `flask routes`


## Running Tests

Use the following `.env` file for running tests:

```
# PostgreSQL Database
DATABASE_URL = sqlite:///:memory:

# Flask
FLASK_APP=src
FLASK_DEBUG=1

# JWT Auth
JWT_SECRET_KEY=super_secret_key
```

Simply run `pytest` in the root directory to run all available tests.

To see coverage of the implemented tests, run the following commands in the root directory:
1. `coverage run -m pytest`
2. `coverage report -m`

For more details see the official [Coverage Documentation](https://coverage.readthedocs.io/en/7.5.4/).