import json
from typing import Union

import pytest
from flask.testing import FlaskClient

from apps.extensions import db
from apps.risks.models import Risk


def test_get_risk_all(client: FlaskClient, token):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.get(
        "/risk", headers={"Authorization": f"Bearer {token['access_token']}"}
    )
    assert response.status_code == 200
    assert len(json.loads(response.data)) > 1


@pytest.mark.parametrize("risk_id", [1, 2])
def test_get_risk_by_id(client: FlaskClient, risk_id: int, token):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.get(
        f"/risk/{risk_id}",
        headers={"Authorization": f"Bearer {token['access_token']}"}
    )
    assert response.status_code == 200
    assert json.loads(response.data) in [
        {'message': 'Not records found'},
        [
            {
                "created_at": "Tue, 27 Jun 2023 23:13:49 GMT",
                "id": 2,
                "risk": "Ransomware",
                "status": True,
                "updated_at": "Sat, 01 Jul 2023 16:34:47 GMT",
            }
        ],
    ]


@pytest.mark.parametrize("risk_id", [1])
def test_get_risk_by_id_not_token(client: FlaskClient, risk_id: int, token):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.get(
        f"/risk/{risk_id}",
        headers={"Authorization": "Bearer "})
    assert response.status_code == 400
    assert json.loads(response.data) == {"error": "Missing bearer token"}


@pytest.mark.parametrize("risk_id", ["a", [1], {"test": 1}])
def test_get_risk_worng_id(
        client: FlaskClient,
        risk_id: Union[str, list, dict],
        token):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.get(
        f"/risk/{risk_id}",
        headers={"Authorization": f"Bearer {token['access_token']}"}
    )
    assert response.status_code == 404


@pytest.mark.parametrize("risk_id", [2])
def test_update_risk(client: FlaskClient, risk_id: int, token, risk_register):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.put(
        f"/risk/{risk_id}",
        data=risk_register,
        headers={"Authorization": f"Bearer {token['access_token']}"},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert json.loads(response.data) == \
        {"message": "Risk updated successfully"}


@pytest.mark.parametrize("risk_id", [1])
def test_update_risk_not_found(
        client: FlaskClient,
        risk_id: int,
        token,
        risk_register):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.put(
        f"/risk/{risk_id}",
        data=risk_register,
        headers={"Authorization": f"Bearer {token['access_token']}"},
        content_type="application/json",
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {"message": "Risk not found"}


def test_delete_risk(app, client: FlaskClient, token):
    with app.app_context():
        new_risk = Risk(risk="Test delete")
        db.session.add(new_risk)
        db.session.commit()
        del token["userinfo"]

        with client.session_transaction() as session:
            session["google_token"] = token

        response = client.delete(
            f"/risk/{new_risk.id}",
            headers={"Authorization": f"Bearer {token['access_token']}"},
            content_type="application/json",
        )
        assert response.status_code == 200
        assert json.loads(response.data) == \
            {"message": "risk deleted successfully"}


@pytest.mark.parametrize("risk_id", [1])
def test_delete_risk_not_found(client: FlaskClient, risk_id: int, token):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.delete(
        f"/risk/{risk_id}",
        headers={"Authorization": f"Bearer {token['access_token']}"},
        content_type="application/json",
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {"message": "Risk not found"}


def test_post_risk(client: FlaskClient, token, risk_register):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.post(
        "/risk",
        data=risk_register,
        headers={"Authorization": f"Bearer {token['access_token']}"},
        content_type="application/json",
    )
    assert response.status_code == 201
    assert json.loads(response.data) == {
        "message": "The risk has been added successfully"
    }
