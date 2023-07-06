import json
from typing import Union

import pytest
from flask.testing import FlaskClient

from apps.extensions import db
from apps.risks.models import RiskHistory


def test_post_risk_history(client: FlaskClient, token, risk_history_register):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.post(
        "/risk_history",
        data=json.dumps(risk_history_register),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        content_type="application/json",
    )
    assert response.status_code == 201
    assert json.loads(response.data) == {
        "message": "The register has been added successfully"
    }


def test_post_risk_history_wrong_user(
    client: FlaskClient, token, risk_history_register
):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    risk_history_register["user_id"] = 0
    response = client.post(
        "/risk_history",
        data=json.dumps(risk_history_register),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        content_type="application/json",
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {"message": "User not found"}


def test_post_risk_history_wrong_risk(
    client: FlaskClient, token, risk_history_register
):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    risk_history_register["risk_id"] = 0
    response = client.post(
        "/risk_history",
        data=json.dumps(risk_history_register),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        content_type="application/json",
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {"message": "Risk not found"}


def test_get_risk_history_all(client: FlaskClient, token):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.get(
        "/risk_history/1",
        headers={"Authorization": f"Bearer {token['access_token']}"}
    )
    assert response.status_code == 200
    assert len(json.loads(response.data)) > 1


@pytest.mark.parametrize("risk_str", ["test"])
def test_get_risk_history_by_str(client: FlaskClient, risk_str: str, token):
    del token["userinfo"]
    pages = 1
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.get(
        f"/risk_history/{risk_str}/{pages}",
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )
    assert response.status_code == 200
    assert len(json.loads(response.data)) >= 1


@pytest.mark.parametrize("risk_str", ["string"])
def test_get_risk_history_by_str_pagination(
        client: FlaskClient,
        risk_str: str, token):
    del token["userinfo"]
    pages = 1
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.get(
        f"/risk_history/{risk_str}/{pages}",
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["meta"]["next_page"] == 2


@pytest.mark.parametrize("risk_id", [2])
def test_get_risk_history_by_id(client: FlaskClient, risk_id: int, token):
    del token["userinfo"]
    pages = 1
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.get(
        f"/risk_history/{risk_id}/{pages}",
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )
    assert response.status_code == 200
    assert len(json.loads(response.data)) >= 1


@pytest.mark.parametrize("risk_id", [3])
def test_get_risk_history_by_id_pagination(
        client: FlaskClient,
        risk_id: int, token):
    del token["userinfo"]
    pages = 1
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.get(
        f"/risk_history/{risk_id}/{pages}",
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["meta"]["next_page"] == 2


@pytest.mark.parametrize(
        "impact, description, title",
        [("meli", "string", "aa")])
def test_get_risk_history_by_multiple_fields(
    client: FlaskClient, impact: str, description: str, title: str, token
):
    del token["userinfo"]
    pages = 1
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.get(
        f"/risk_history/{impact}/{description}/{title}/{pages}",
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )
    assert response.status_code == 200
    assert json.loads(response.data) == \
        {"message": "Not records found"}


@pytest.mark.parametrize(
        "impact, description, title",
        [("string", "string", "string")])
def test_get_risk_history_by_multiple_fields_pagination(
    client: FlaskClient, impact: str, description: str, title: str, token
):
    del token["userinfo"]
    pages = 1
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.get(
        f"/risk_history/{impact}/{description}/{title}/{pages}",
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["meta"]["next_page"] == 2


@pytest.mark.parametrize("risk_history_id", [1])
def test_update_risk_history(
    client: FlaskClient, risk_history_id: int, token, risk_history_register
):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.put(
        f"/risk_history/{risk_history_id}",
        data=json.dumps(risk_history_register),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert json.loads(response.data) == \
        {"message": "Risk history updated successfully"}


@pytest.mark.parametrize("risk_history_id", [0])
def test_update_risk_history_not_found(
    client: FlaskClient, risk_history_id: int, token, risk_history_register
):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.put(
        f"/risk_history/{risk_history_id}",
        data=json.dumps(risk_history_register),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        content_type="application/json",
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {"message": "Risk history not found"}


@pytest.mark.parametrize(
    "risk_history_id, key, value",
    [
        (2, "title", "Test"),
        (2, "impact", "Test"),
        (2, "probability", 100),
        (2, "description", "Test"),
        (2, "risk_id", 2),
    ],
)
def test_patch_risk_history(
        client: FlaskClient,
        risk_history_id: int,
        key: str,
        value: Union[str, int],
        token):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.patch(
        f"/risk_history/{risk_history_id}",
        data=json.dumps({key: value}),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert json.loads(response.data) == \
        {"message": "Risk history updated successfully"}


@pytest.mark.parametrize("risk_history_id, key, value", [(0, "title", "Test")])
def test_patch_risk_history_not_found(
        client: FlaskClient,
        risk_history_id: int,
        key: str,
        value: Union[str, int], token):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.patch(
        f"/risk_history/{risk_history_id}",
        data=json.dumps({key: value}),
        headers={"Authorization": f"Bearer {token['access_token']}"},
        content_type="application/json",
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {"message": "Risk history not found"}


def test_delete_risk_history(
        app, client: FlaskClient, token, risk_history_register):
    del token["userinfo"]
    with app.app_context():
        new_risk_history = RiskHistory(**risk_history_register)
        db.session.add(new_risk_history)
        db.session.commit()

        with client.session_transaction() as session:
            session["google_token"] = token

        response = client.delete(
            f"/risk_history/{new_risk_history.id}",
            headers={"Authorization": f"Bearer {token['access_token']}"},
            content_type="application/json",
        )
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "message": "Risk history deleted successfully"
        }


def test_delete_risk_history_not_found(
    app, client: FlaskClient, token, risk_history_register
):
    del token["userinfo"]
    with client.session_transaction() as session:
        session["google_token"] = token

    response = client.delete(
        "/risk_history/0",
        headers={"Authorization": f"Bearer {token['access_token']}"},
        content_type="application/json",
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {"message": "Risk history not found"}
