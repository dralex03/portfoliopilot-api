from flask.cli import FlaskGroup
from src.database.setup import create_db_schema
from src import create_app


if __name__ == "__main__":
    # Create app
    app = create_app()
    cli = FlaskGroup(app)

    # Setup database and start flask app
    create_db_schema()
    cli()


