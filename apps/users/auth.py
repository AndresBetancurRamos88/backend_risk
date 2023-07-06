from typing import Dict

from flasgger import swag_from
from flask import Blueprint, make_response, redirect, request, session, url_for
from flask_cors import cross_origin
from flask.json import jsonify
from flask_restful import Resource

from apps.common.utils import login_required
from apps.extensions import db, oauth

from .models import User

auth = Blueprint("auth", __name__)


class Login(Resource):
    def get(self):
        google = oauth.create_client("google")
        # create the google oauth client
        redirect_uri = url_for("authorize", _external=True)
        session["origin_url"] = request.headers.get("Referer")
        return make_response(google.authorize_redirect(redirect_uri), 302)


import pytest
class Authorize(Resource):
    @cross_origin(origin="http://localhost:3000")
    def get(self):
        google = oauth.create_client("google")
        token = google.authorize_access_token()
        self.validate_user(token)
        session["google_token"] = token
        # pytest.set_trace()
        # make the session permanant so it keeps existing
        # after broweser gets close
        # session.permanent = True
        # if the request doenst comes from swagger, it returns the token
        origin_url = session.get("origin_url") 
        if origin_url in ["http://localhost:3000/", "http://127.0.0.1:3000"] :
            return make_response(redirect("http://localhost:3000/"), 302)

        if not origin_url:
            return make_response(redirect("/token"), 302)

        return make_response(redirect(
            url_for("flasgger.oauth_redirect")), 302)

    def validate_user(self, token_info: Dict) -> None:
        filtered_data = {
            key: value
            for key, value in token_info["userinfo"].items()
            if hasattr(User, key) and key != "id"
        }
        user = User.query.filter_by(
            email=token_info["userinfo"]["email"]).first()
        
        if not user:
            user = User(**filtered_data)
            db.session.add(user)
            db.session.commit()

        token_info["userinfo"]["user_id"] = user.id

class Logout(Resource):
    def get(self):
        for key in list(session.keys()):
            session.pop(key)
        referer = request.headers.get("Referer")
        if referer:
            if referer.split("/")[-1] == "api-docs":
                return make_response(
                    redirect(url_for("flasgger.oauth_redirect")), 302)
        return make_response({"message": "Logged out successfully"}, 200)


class Token(Resource):
    @login_required
    @swag_from("auth_swagger.yml")
    def get(self):
        token = dict(session).get("google_token")
        return make_response(jsonify(token),200)
