import os
from datetime import timedelta

BASE_DIR= os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Risks API",
        "description": "API for Meli risks",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "andres-ramos88@hotmail.com",
            "url": "https://www.linkedin.com/in/andres-betancur-ramos-14b35b49/",
        },
        "termsOfService": "https://www.linkedin.com/in/andres-betancur-ramos-14b35b49/",
        "version": "1.0"
    },
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "google_auth_login": {
            "type": "oauth2",
            "description": "Autenticación de Google con inicio de sesión requerido",
            "flow": "implicit",
            "authorizationUrl": "/login",
            "tokenUrl": "/token",
            "scopes": {
                "email": "Acceso a la dirección de correo electrónico del usuario.",
                "profile": "Acceso al perfil básico del usuario."
            }
        },
    },
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api-docs"
}


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_NAME = "google-login-session"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'risk-dev.db')}"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'risk.db')}"


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

REGISTERS_BY_PAGE = 5