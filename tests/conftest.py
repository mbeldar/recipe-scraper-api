"""Pytest configuration and fixtures."""

import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    """Create and configure a test Flask app."""
    from src.api import app
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
