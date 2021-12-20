import os
import tempfile

import pytest

from app.app import app
from app.database.migration.MongoInit import MongoInit


@pytest.fixture
def client():
    """init with a test."""
    db_fd, db_path = tempfile.mkstemp()
    # app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            MongoInit().init_db_index()
        yield client

    os.close(db_fd)
    os.unlink(db_path)
