import os
import uuid

import psycopg
import pytest
from psycopg import sql
from psycopg.rows import dict_row

from repository import Repository


@pytest.fixture(autouse=True)
def isolated_database_schema(monkeypatch):
    """Run every test against real PostgreSQL without touching existing tasks."""
    url = os.environ['DATABASE_URL']
    schema = 'test_' + uuid.uuid4().hex
    with psycopg.connect(url, autocommit=True) as db:
        db.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(schema)))
    monkeypatch.setattr(
        Repository,
        'connect',
        lambda self: psycopg.connect(url, row_factory=dict_row, options=f'-c search_path={schema}'),
    )
    try:
        yield
    finally:
        with psycopg.connect(url, autocommit=True) as db:
            db.execute(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(schema)))
