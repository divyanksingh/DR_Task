from flask.views import MethodView
from flask import make_response
from helpers.auth_token import token_required
import uuid
import json


class Resource(MethodView):
    GET_URL_LIST = []
    POST_URL_LIST = []
    DELETE_URL_LIST = []
    PUT_URL_LIST = []
    DECORATORS_LIST = []

def json_marshal(view_func):
    def decorator(*args, **kwargs):
        result = view_func(*args, **kwargs)
        if isinstance(result, tuple):
            status = result[0]
            data = result[1]
            headers = result[2]
            response = make_response(json.dumps(data), status)
            for key, val in headers.items():
                response.headers[key] = val
            return response
        else:
            return result
    return decorator

def AddResource(cls):
    app = cls.BLUEPRINT
    default_decorators = [json_marshal]
    view = cls.as_view(str(cls))
    version_number = cls.VERSION
    version = "/v" + str(version_number)

    for url in cls.GET_URL_LIST:
        url = version + url
        if 'GET' in cls.AUTH_REQUIRED:
            default_decorators = [token_required, json_marshal]
        decorators_list = cls.DECORATORS_LIST + default_decorators
        for decorator in decorators_list:
            view = decorator(view)
        endpoint = str(uuid.uuid4())
        app.add_url_rule(
                url, endpoint=endpoint, defaults={"id": None},
                view_func=view, methods=['GET']
        )

    for url in cls.POST_URL_LIST:
        url = version + url
        if 'POST' in cls.AUTH_REQUIRED:
            default_decorators = [token_required, json_marshal]
        decorators_list = cls.DECORATORS_LIST + default_decorators
        for decorator in decorators_list:
            view = decorator(view)
        endpoint = str(uuid.uuid4())
        app.add_url_rule(
                url, endpoint=endpoint,
                view_func=view, methods=['POST']
        )

    for url in cls.DELETE_URL_LIST:
        url = version + url
        if 'DELETE' in cls.AUTH_REQUIRED:
            default_decorators = [token_required, json_marshal]
        decorators_list = cls.DECORATORS_LIST + default_decorators
        for decorator in decorators_list:
            view = decorator(view)
        endpoint = str(uuid.uuid4())
        app.add_url_rule(
                url, endpoint=endpoint,
                view_func=view, methods=['DELETE']
        )

    for url in cls.PUT_URL_LIST:
        url = version + url
        if 'PUT' in cls.AUTH_REQUIRED:
            default_decorators = [token_required, json_marshal]
        decorators_list = cls.DECORATORS_LIST + default_decorators
        for decorator in decorators_list:
            view = decorator(view)
        endpoint = str(uuid.uuid4())
        app.add_url_rule(
                url, endpoint=endpoint,
                view_func=view, methods=['PUT']
        )


def register_url(class_name):
    for cls in type.__subclasses__(class_name):
        AddResource(cls)