from flask.cli import FlaskGroup

from src.database.connection import create_database
from src import api


cli = FlaskGroup(api)

if __name__ == "__main__":
    create_database()
    cli()
