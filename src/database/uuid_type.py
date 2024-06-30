import uuid

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.types import CHAR, TypeDecorator


class UUID(TypeDecorator):
    """
    Custom Version of UUID Type that implements the type either as UUID
    from the postgresql dialect or as a normal String (CHAR(36)).
    This has no effect on how PostgreSQL will treat UUIDs, but it enables
    writing tests with SQLite in-memory database.
    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)
