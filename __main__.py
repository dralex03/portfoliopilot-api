from flask.cli import FlaskGroup

from src import api

cli = FlaskGroup(api)


if __name__ == "__main__":
    cli()