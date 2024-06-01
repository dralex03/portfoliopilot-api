from flask.cli import FlaskGroup
from src.database.setup import setup_database
from src import api

cli = FlaskGroup(api)

if __name__ == "__main__":
    setup_database()
    cli()


