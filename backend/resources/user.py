from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.user import User
from utils import hash_password
from flask_jwt_extended import jwt_required, get_jwt_identity

class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        username = json_data.get('username')
        name = json_data.get('name')
        email = json_data.get('email')
        non_hash_password = json_data.get('password')
        bio = json_data.get('bio')

        if User.get_by_username(username):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST
        
        if User.get_by_email(email):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST
        
        password = hash_password(non_hash_password)

        user = User(
            username=username,
            name=name,
            email=email,
            password=password,
            bio=bio
        ) 

        user.save()

        data = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email
        }

        return data, HTTPStatus.CREATED
    
class UserResource(Resource):
    @jwt_required(optional=True, fresh=False)
    def get(self, username):
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user == user.id:
            data = {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'bio': user.bio,
                
            } 
        else:
            data = {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'bio': user.bio
            }
        
        return data, HTTPStatus.OK
    
class MeResource(Resource):
    @jwt_required(fresh=False)
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        data = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'bio': user.bio            
        }
    
        return data, HTTPStatus.OK
    
