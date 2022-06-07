"""Initialize the testing environment

Creates an app for testing that has the configuration flag TESTING set to True.
"""

import pytest

from flaskr.main import app


@pytest.fixture
def client():
    """Configures the app for testing

    :return: App for testing
    """

    app.config['TESTING'] = True
    client = app.test_client()

    yield client
