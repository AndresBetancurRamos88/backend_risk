from decimal import Decimal

from flasgger import swag_from
from flask import Blueprint, make_response
from flask_restful import Resource, reqparse

from apps.common.utils import invalidate_cache, login_required, query_set
from apps.config import REGISTERS_BY_PAGE
from apps.extensions import cache, db
from apps.users.models import User

from ..models import Risk, RiskHistory

risk_history = Blueprint("risk_history", __name__)


class RiskHistoryResourceByStr(Resource):
    @login_required
    @swag_from("../docs/risks_history/get_risk_history_by_str_swagger.yml")
    def get(self, risk_str: str = None, page: int = 1):
        # Creating cache
        cache_key = f"history_risk_by_str_{risk_str}_{page}"
        result = cache.get(cache_key)
        if result is None:
            queryset = (RiskHistory.query
                .join(User)
                .join(Risk)
                .with_entities(
                    RiskHistory.id,
                    Risk.risk,
                    RiskHistory.title,
                    RiskHistory.description,
                    RiskHistory.impact,
                    RiskHistory.probability,
                    User.email,
                    RiskHistory.created_at,
                    RiskHistory.updated_at
                )
                .filter(
                    db.or_(
                        RiskHistory.title.ilike(f"%{risk_str}%"),
                        RiskHistory.description.ilike(f"%{risk_str}%"),
                    )
                ).paginate(page=page, per_page=REGISTERS_BY_PAGE)
            )
            if not queryset.items:
                return {"message": "Not records found"}, 200
            
            columns = queryset.items[0]._fields
            data = query_set(queryset, columns, True)
            cache.set(cache_key, data)
            return make_response(data, 200)
        return make_response(result, 200)


class RiskHistoryResourceById(Resource):
    @login_required
    @swag_from("../docs/risks_history/get_risk_history_by_id_swagger.yml")
    def get(self, risk_id: int = None, page: int = 1):
        # Creating cache
        cache_key = f"history_risk_by_id_{risk_id}_{page}"
        result = cache.get(cache_key)
        if result is None:
            queryset = (RiskHistory.query
                .join(User)
                .join(Risk)
                .with_entities(
                    RiskHistory.id,
                    Risk.risk,
                    RiskHistory.title,
                    RiskHistory.description,
                    RiskHistory.impact,
                    RiskHistory.probability,
                    User.email,
                    RiskHistory.created_at,
                    RiskHistory.updated_at
                )                
                .filter_by(risk_id=risk_id).paginate(
                page=page, per_page=REGISTERS_BY_PAGE
            ))
            
            if not queryset.items:
                return {"message": "Not records found"}, 200
            
            columns = queryset.items[0]._fields
            data = query_set(queryset, columns, True)
            cache.set(cache_key, data)
            return make_response(data, 200)
        return make_response(result, 200)


class RiskHistoryResourceByMultipleFields(Resource):
    @login_required
    @swag_from("../docs/risks_history/get_risk_history_by_multiple_fields_swagger.yml")
    def get(self, impact: str, description: str, title: str, page: int = 1):
        # Creating cache
        cache_key = f"history_risk_multiple_str_{impact}_{description}_{title}_{page}"
        result = cache.get(cache_key)
        if result is None:
            query = RiskHistory.query\
                .join(User)\
                .join(Risk)\
                .with_entities(
                    RiskHistory.id,
                    Risk.risk,
                    RiskHistory.title,
                    RiskHistory.description,
                    RiskHistory.impact,
                    RiskHistory.probability,
                    User.email,
                    RiskHistory.created_at,
                    RiskHistory.updated_at
                )
            if impact and impact != "undefined":
                query = query.filter(
                    RiskHistory.impact.ilike(f"%{impact}%"))
            if description and description != "undefined":
                query = query.filter(
                    RiskHistory.description.ilike(f"%{description}%"))
            if title and title != "undefined":
                query = query.filter(
                    RiskHistory.title.ilike(title))

            queryset = query.paginate(page=page, per_page=REGISTERS_BY_PAGE)

            if not queryset.items:
                return {"message": "Not records found"}, 200

            columns = queryset.items[0]._fields
            data = query_set(queryset, columns, True)
            cache.set(cache_key, data)
            return make_response(data, 200)
        return make_response(result, 200)


class RiskHistoryResourceModify(Resource):
    @login_required
    @swag_from("../docs/risks_history/put_risk_history_swagger.yml")
    def put(self, risk_history_id: int):
        # Get the data from the request body
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True)
        parser.add_argument("impact", type=str, required=True)
        parser.add_argument("probability", type=Decimal, required=True)
        parser.add_argument("description", type=str, required=True)
        parser.add_argument("risk_id", type=int, required=True)
        args = parser.parse_args()
        # Risk history search by Id in the database
        risk_history = RiskHistory.query.get(risk_history_id)
        if not risk_history:
            return {"message": "Risk history not found"}, 404

        # Update risk history fields
        risk_history.title = args["title"]
        risk_history.impact = args["impact"]
        risk_history.probability = args["probability"]
        risk_history.description = args["description"]
        risk_history.risk_id = args["risk_id"]

        try:
            # Save changes in  database
            db.session.commit()
            # Delete cache because the data was modified
            invalidate_cache("risk")
            return {"message": "Risk history updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @login_required
    @swag_from("../docs/risks_history/patch_risk_history_swagger.yml")
    def patch(self, risk_history_id: int):
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str)
        parser.add_argument("impact", type=str)
        parser.add_argument("probability", type=Decimal)
        parser.add_argument("description", type=str)
        parser.add_argument("risk_id", type=int)
        args = parser.parse_args()

        # Risk history search by Id in the database
        risk_history = RiskHistory.query.get(risk_history_id)
        if not risk_history:
            return {"message": "Risk history not found"}, 404

        # Update risk history fields if provided in the request
        if args["title"]:
            risk_history.title = args["title"]
        if args["impact"]:
            risk_history.impact = args["impact"]
        if args["probability"] or args["probability"] == 0:
            risk_history.probability = args["probability"]
        if args["description"]:
            risk_history.description = args["description"]
        if args["risk_id"]:
            risk_history.risk_id = args["risk_id"]

        try:
            # Save changes in database
            db.session.commit()
            # Delete cache because the data was modified
            invalidate_cache("risk")
            return {"message": "Risk history updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @login_required
    @swag_from("../docs/risks_history/delete_risk_history_swagger.yml")
    def delete(self, risk_history_id: int):
        risk_history = RiskHistory.query.get(risk_history_id)
        if risk_history:
            try:
                db.session.delete(risk_history)
                db.session.commit()
                invalidate_cache("history_risk")
                return {"message": "Risk history deleted successfully"}
            except Exception as e:
                return {"error": str(e)}, 500
        else:
            return {"message": "Risk history not found"}, 404


class RiskHistoryResourceAll(Resource):
    @login_required
    @swag_from("../docs/risks_history/get_risk_history_swagger.yml")
    def get(self, page: int = 1):
        cache_key = f"history_risk_{page}"
        result = cache.get(cache_key)
        if result is None:
            queryset = (
                db.session.query(
                RiskHistory.id,
                Risk.risk,
                RiskHistory.title,
                RiskHistory.description,
                RiskHistory.impact,
                RiskHistory.probability,
                User.email,
                RiskHistory.created_at,
                RiskHistory.updated_at
                )
                .join(User)
                .join(Risk)
            ).paginate(page=page, per_page=REGISTERS_BY_PAGE)

            if not queryset.items:
                return {"message": "Not records found"}, 200
            
            columns = queryset.items[0]._fields
            data = query_set(queryset, columns, True)
            cache.set(cache_key, data)
            return make_response(data, 200)
        return make_response(result, 200)


class RiskHistoryResource(Resource):
    @login_required
    @swag_from("../docs/risks_history/post_risk_history_swagger.yml")
    def post(self):
        # Get the data from the request body
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True)
        parser.add_argument("impact", type=str, required=True)
        parser.add_argument("probability", type=float, required=True)
        parser.add_argument("description", type=str, required=True)
        parser.add_argument("risk_id", type=int, required=True)
        parser.add_argument("user_id", type=int, required=True)
        args = parser.parse_args()

        risk = Risk.query.get(args["risk_id"])
        if not risk:
            return {"message": "Risk not found"}, 404

        user = User.query.get(args["user_id"])
        if not user:
            return {"message": "User not found"}, 404

        try:
            # Create an instance of Risk model
            new_risk_history = RiskHistory(
                title=args["title"],
                impact=args["impact"],
                probability=args["probability"],
                description=args["description"],
                risk_id=args["risk_id"],
                user_id=args["user_id"],
            )
            db.session.add(new_risk_history)
            # Save changes in  database
            db.session.commit()
            invalidate_cache("history_risk")
            return {"message": "The register has been added successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500
