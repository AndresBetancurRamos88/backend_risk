from typing import Dict

from flasgger import swag_from
from flask import Blueprint, make_response, redirect, session, url_for
from flask_restful import Resource
from flask.json import jsonify

from apps.common.utils import login_required
from apps.extensions import db, oauth
from .models import User

auth = Blueprint('auth', __name__)


class Login(Resource):
    def get(self):
        google = oauth.create_client('google')
        redirect_uri = url_for('authorize', _external=True)
        return google.authorize_redirect(redirect_uri)


class Authorize(Resource):
    def get(self):  
        google = oauth.create_client('google')  # create the google oauth client
        token = google.authorize_access_token()  # Access token from google (needed to get user info)
        self.validate_user(token)
        session['google_token'] = token
        session.permanent = True  # make the session permanant so it keeps existing after broweser gets closedcl
        return redirect(url_for("flasgger.oauth_redirect"))
    
    def validate_user(self, token_info:Dict) -> None:
        filtered_data = {key: value for key, value in token_info["userinfo"].items() if hasattr(User, key) and key != "id"}
        user = User.query.filter_by(email=token_info["userinfo"]["email"]).first()
        if not user:
            user = User(**filtered_data)
            db.session.add(user)
            db.session.commit()


class Token(Resource):
    @login_required    
    @swag_from('auth_swagger.yml')
    def get(self):
        token = dict(session).get("google_token")
        return  make_response(jsonify({
            "access_token": token["access_token"],
            "expires_in": token["expires_in"],
            "id_token": token["id_token"],
            "scope": token["scope"],
            "token_type": token["token_type"]
        }), 200)
        