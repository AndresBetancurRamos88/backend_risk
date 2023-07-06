import json
from unittest.mock import MagicMock

import pytest
from dotenv import load_dotenv
from flask import Flask
from flask.testing import FlaskClient

from apps import create_app
from apps.extensions import oauth

# Carga las variables de entorno desde .flaskenv
load_dotenv(".flaskenv")


@pytest.fixture
def app() -> Flask:
    app_test = create_app()
    app_test.config["SERVER_NAME"] = "localhost"
    app_test.config["APPLICATION_ROOT"] = "/"
    app_test.config["PREFERRED_URL_SCHEME"] = "http"
    return app_test


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    with app.test_client() as client:
        yield client


@pytest.fixture
def token():
    return {
        "access_token": "123456789",
        "expires_in": 3599,
        "id_token": "",
        "scope": "https://www.googleapis.com/auth/userinfo.profile openid https://www.googleapis.com/auth/userinfo.email",
        "token_type": "Bearer",
        "userinfo": {
            "email": "test_user@test.com",
            "given_name": "test",
            "family_name": "user",
        },
    }


@pytest.fixture
def mock_authorize(token):
    google_client = oauth.create_client("google")
    mock_token = MagicMock(return_value=token)
    google_client.authorize_access_token = mock_token
    return google_client


@pytest.fixture
def risk_register():
    return json.dumps({"risk": "Ransomware", "status": True})


@pytest.fixture
def risk_history_register():
    return {
        "title": "Test risk",
        "impact": "High",
        "probability": 10.10,
        "description": "Test description",
        "risk_id": 2,
        "user_id": 2,
    }
