from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.user import User
from utils import hash_password

class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        username = json_data.get('username')
        name = json_data.get('name')
        email = json_data.get('email')
        non_hash_password = json_data.get('password')

        if User.get_by_username(username):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST
        
        if User.get_by_email(email):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST
        
        password = hash_password(non_hash_password)

        user = User(
            username=username,
            name=name,
            email=email,
            password=password
        ) 

        user.save()

        data = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email
        }

        return data, HTTPStatus.CREATED