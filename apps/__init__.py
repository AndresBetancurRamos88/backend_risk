import os

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from .config import config, swagger_config, swagger_template
from .extensions import cache, db, migrate, oauth
from .risks.routes.risk_history_routes import (
    RiskHistoryResource,
    RiskHistoryResourceAll,
    RiskHistoryResourceById,
    RiskHistoryResourceByMultipleFields,
    RiskHistoryResourceByStr,
    RiskHistoryResourceModify,
    risk_history,
)
from .risks.routes.risk_routes import RiskResource, RiskResourceById, risk
from .users.auth import Authorize, Login, Logout, Token, auth


def create_app():
    app = Flask(__name__)
    app.config.from_object(config[os.getenv("FLASK_ENV")])
    config[os.getenv("FLASK_ENV")].init_app(app)
    api = Api(app)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    Swagger(app, config=swagger_config, template=swagger_template)

    app.register_blueprint(auth)
    app.register_blueprint(risk)
    app.register_blueprint(risk_history)

    api.add_resource(Login, "/login")
    api.add_resource(Authorize, "/authorize")
    api.add_resource(Logout, "/logout")
    api.add_resource(Token, "/token")
    api.add_resource(RiskResource, "/risk")
    api.add_resource(RiskResourceById, "/risk/<int:risk_id>")
    api.add_resource(RiskHistoryResource, "/risk_history")
    api.add_resource(
        RiskHistoryResourceAll,
        "/risk_history/<int:page>"
    )
    api.add_resource(
        RiskHistoryResourceModify,
        "/risk_history/<int:risk_history_id>"
    )
    api.add_resource(
        RiskHistoryResourceById,
        "/risk_history/<int:risk_id>/<int:page>"
    )
    api.add_resource(
        RiskHistoryResourceByStr, "/risk_history/<string:risk_str>/<int:page>"
    )
    api.add_resource(
        RiskHistoryResourceByMultipleFields,
        "/risk_history/<string:impact>/<string:description>/<string:title>/<int:page>",
    )

    db.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)
    return app
