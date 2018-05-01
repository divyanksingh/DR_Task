from flask import Blueprint, request
from controllers.user.base import (
	BaseUserCrud, BaseUserLogin
)
from helpers.auth_token import tokenize
from application.extensions import db
from rest.restfull import register_url
from models.users import UserInfo
import json


user_version1 = Blueprint('user_version1', __name__)


class Version1(object):
    VERSION = 1
    BLUEPRINT = user_version1


class UserCRUD(Version1, BaseUserCrud):

    def get(self, id):
        if id is None:
        	user_list = []
        	users = db.session.query(UserInfo).all()
        	for user in users:
        		user_list.append({
        			"name": user.display_name,
        			"username": user.username
        			})
        	return (200, {"user_list": user_list}, {})

        else:
            user = db.session.query(UserInfo).get(id)
            if not user:
                return (404, {"message": "User not found"}, {})    
            return (200, {"name": user.display_name, "username": user.username}, {})

    def post(self):
        data = json.loads(request.data.decode('utf-8'))
        display_name = data.get('display_name', None)
        username = data.get('username', None)
        if not username:
            return (422, {"message": "username is mandatory"}, {})
        password = data.get('password')
        user = UserInfo()
        user.username = username
        user.display_name = display_name
        user.update_password(password)
        db.session.add(user)
        db.session.commit()
        return (201, {"user_id": user.id}, {})

    def delete(self, id):
        user = db.session.query(UserInfo).get(id)
        if not user:
            return (404, {"message": "User not found"}, {}) 
        db.session.delete(user)
        db.session.commit()
        return (200, {}, {})


    def put(self, id):
        data = json.loads(request.data.decode('utf-8'))
        display_name = data.get('display_name', None)
        password = data.get('password', None)
        user = db.session.query(UserInfo).get(id)
        if not user:
            return (404, {"message": "User not found"}, {}) 
        if display_name:
            user.display_name = display_name
        if password:
            user.update_password(password)
        db.session.add(user)
        db.session.commit()
        return (200, {}, {})


class Login(Version1, BaseUserLogin):

    def fetch_data(self):
        data = json.loads(request.data.decode('utf-8'))
        username = data.get('username').lower()
        password = data.get('password').lower()
        return username, password

    def get_token(self, user):
        payload = {
                "user_id": user.id,
                "username": user.username,
        }
        token = tokenize(payload)
        return token

    def authenticate(self, username, password):
        query = db.session.query(UserInfo).filter(
                    UserInfo.username == username)
        user = query.first()
        if user.has_password(password):
        	token = self.get_token(user)

        return {"token": token.decode('utf-8')}

    def post(self):
        username, password = self.fetch_data()
        result = self.authenticate(username, password)
        return (200, result, {})



register_url(Version1)