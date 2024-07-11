# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    # opens temp file; returns file descriptor and path to it
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,  # Database path is overwritten
        }
    )

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
