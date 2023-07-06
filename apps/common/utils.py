from functools import wraps
from typing import List, Tuple, Union

from flask import current_app, jsonify, make_response, request, session
from sqlalchemy import inspect

from apps.extensions import cache, db


def invalidate_cache(prefix: str):
    with current_app.app_context():
        for key in list(cache.cache._cache.keys()):
            if key.startswith(prefix):
                cache.delete(key)


def query_set(queryset, columns: Union[List, Tuple], paginated: bool = False):
    data_json = []
    for element in queryset:
        json_element = {}
        for column in columns:
            column_name = column
            value = getattr(element, column_name)
            json_element[column_name] = value
        data_json.append(json_element)

    if not paginated:
        return jsonify(data_json)

    meta = {
        "page": queryset.page,
        "pages": queryset.pages,
        "total_count": queryset.total,
        "prev_page": queryset.prev_num,
        "next_page": queryset.next_num,
        "has_prev": queryset.has_prev,
        "has_next": queryset.has_next,
    }
    return jsonify({"data": data_json, "meta": meta})


def login_required(func):
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        token = dict(session).get("google_token")
        """
        Token matching is validated when it is a different
        endpoint than token
        """
        if not token:
            return make_response(
                jsonify({"error": "login required"}), 401)

        if request.url.split("/")[-1] != "token":
            try:
                bearer_token = request.headers.get("Authorization").split()[1]
            except IndexError:
                return make_response(
                    jsonify({"error": "Missing bearer token"}), 400)
            except (AttributeError, TypeError):
                return make_response(
                    jsonify({"error": "login required"}), 401)
            if token["access_token"] != bearer_token:
                return make_response(
                    jsonify({"error": "Wrong token"}), 401)

        return func(*args, **kwargs)

    return wrapper_function
