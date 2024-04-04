from http import HTTPStatus
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                jwt_required, get_jwt_identity, get_jwt)
from utils import check_password
from models.user import User
from models.token import TokenBlocklist
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
        refresh_token = create_refresh_token(identity=user.id)


        return {
            'access_token': access_token,
            'access_token_expires_in': int((datetime.datetime.now() + datetime.timedelta(minutes=15)).timestamp()),
            'refresh_token': refresh_token,
            'refresh_token_expires_in': int((datetime.datetime.now() + datetime.timedelta(days=30)).timestamp())
        }, HTTPStatus.OK
    
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)

        return {
            'access_token': access_token,
            'access_token_expires_in': int((datetime.datetime.now() + datetime.timedelta(minutes=15)).timestamp())
        }, HTTPStatus.OK

class RevokeResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        token_blocklist = TokenBlocklist()
        token_blocklist.jti = jti
        token_blocklist.token_type = 'access'
        token_blocklist.user_identity = get_jwt_identity()
        token_blocklist.revoked = True
        token_blocklist.save()

        return {}, HTTPStatus.OK 

        