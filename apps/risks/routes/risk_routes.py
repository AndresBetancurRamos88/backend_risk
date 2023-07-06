from flasgger import swag_from
from flask import Blueprint, make_response
from flask_restful import Resource, reqparse

from apps.common.utils import invalidate_cache, login_required, query_set
from apps.extensions import cache, db

from ..models import Risk

risk = Blueprint("risk", __name__)


class RiskResourceById(Resource):
    @login_required
    @swag_from("../docs/risks/get_risk_by_id_swagger.yml")
    def get(self, risk_id: int = None):
        # Creating cache
        cache_key = f"risk_by_id_{risk_id}"
        result = cache.get(cache_key)
        if result is None:
            queryset = Risk.query.filter_by(id=risk_id)
            if not queryset.count():
                return {"message": "Not records found"}, 200

            columns = Risk.__table__.columns.keys()
            data = query_set(queryset, columns)
            cache.set(cache_key, data)
            return make_response(data, 200)
        return make_response(result, 200)

    @login_required
    @swag_from("../docs/risks/put_risk_swagger.yml")
    def put(self, risk_id: int):
        # Get the data from the request body
        parser = reqparse.RequestParser()
        parser.add_argument("risk", type=str, required=True)
        parser.add_argument("status", type=bool, required=True)
        args = parser.parse_args()

        # Risk search by Id in the database
        risk = Risk.query.filter_by(id=risk_id).first()
        if not risk:
            return {"message": "Risk not found"}, 404

        # Update risk fields
        risk.risk = args["risk"]
        risk.status = args["status"]

        try:
            # Save changes in  database
            db.session.commit()
            # Delete cache because the data was modified
            invalidate_cache("risk")
        except Exception as e:
            return {"error": str(e)}, 500
        return {"message": "Risk updated successfully"}, 200

    @login_required
    @swag_from("../docs/risks/delete_risk_swagger.yml")
    def delete(self, risk_id: int):
        risk = Risk.query.get(risk_id)
        if risk:
            try:
                db.session.delete(risk)
                db.session.commit()
                invalidate_cache("risk")
                return {"message": "risk deleted successfully"}, 200
            except Exception as e:
                return {"error": str(e)}, 500
        else:
            return {"message": "Risk not found"}, 404


class RiskResource(Resource):
    @login_required
    @swag_from("../docs/risks/get_risk_swagger.yml")
    def get(self):
        result = cache.get("risks")
        if result is None:
            queryset = Risk.query.all()
            if not queryset:
                return {"message": "Not records found"}, 200

            columns = Risk.__table__.columns.keys()
            data = query_set(queryset, columns)
            cache.set("risks", data)
            return make_response(data, 200)
        return make_response(result, 200)

    @login_required
    @swag_from("../docs/risks/post_risk_swagger.yml")
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("risk", type=str, required=True)
        args = parser.parse_args()
        try:
            new_risk = Risk(risk=args["risk"])
            db.session.add(new_risk)
            db.session.commit()
            invalidate_cache("risk")
            return {"message": "The risk has been added successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500
