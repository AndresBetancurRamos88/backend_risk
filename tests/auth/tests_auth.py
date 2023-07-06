import json
from unittest.mock import MagicMock

from flask import session, url_for

from apps.extensions import oauth


def test_login(app, client):
    with app.app_context():
        oauth.create_client = MagicMock(return_value=MagicMock())
        response = client.get(url_for("login"))
        assert response.status_code == 302
        assert session.get("origin_url") is None


def test_authorize(app, client, mock_authorize):
    with app.app_context():
        response = client.get(url_for("authorize"))
        assert response.status_code == 302
        assert session.get("google_token")


def test_logout(app, client, mock_authorize):
    with app.app_context():
        response = client.get(url_for("logout"))
        assert response.status_code == 200
        assert session.get("google_token") is None
        assert json.loads(response.data) == \
            {"message": "Logged out successfully"}
