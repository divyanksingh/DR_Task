import datetime
from functools import wraps
from flask import current_app as app
from flask import request
import jwt

def tokenize(payload):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    payload["exp"] = expiration_time
    token = jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )
    return token


def token_required(f):
    @wraps(f)
    def token_validation(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if auth_token:
            try:
                payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            except Exception as e:
                return (401, {"message": "Could not authorize user"}, {})
            result = f(*args, **kwargs)
            print(result)
            return result
        else:
            return (422, {"message": "Auth token not supplied"}, {})

    return token_validation