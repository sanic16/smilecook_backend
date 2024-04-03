from http import HTTPStatus
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from utils import check_password
from models.user import User
import datetime

class TokenResource(Resource):

    def post(self):
        json_data = request.get_json()

        email = json_data.get('email')
        password = json_data.get('password')
        
        user = User.get_by_email(email=email)

        if not user or not check_password(password, user.password):
            return {'message': 'email or password is incorrect'}, HTTPStatus.UNAUTHORIZED
        
        access_token = create_access_token(identity=user.id, fresh=True)

        return {
            'access_token': access_token,
            'access_token_expires_in': int((datetime.datetime.now() + datetime.timedelta(minutes=15)).timestamp())
        }, HTTPStatus.OK
    
    