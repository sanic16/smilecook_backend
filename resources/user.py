from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.user import User
from models.recipe import Recipe
from utils import hash_password, upload_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.user import UserSchema
from schemas.recipe import RecipeSchema
from marshmallow import ValidationError
from webargs import fields, validate
from webargs.flaskparser import use_args

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', 'is_active', 'is_admin'))

recipe_list_schema = RecipeSchema(many=True)

class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        try:
            data = user_schema.load(data= json_data)
        except ValidationError as error:
            return {
                'message': 'Validation error',
                'errors': error.messages
            }, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get('username')):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST
        
        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST
        
        
        user = User(**data) 

        user.save()     

        return user_schema.dump(user), HTTPStatus.CREATED 
    
class UserResource(Resource):
    @jwt_required(optional=True, fresh=False)
    def get(self, username):
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user)
        else:
            data = user_public_schema.dump(user)
        
        return data, HTTPStatus.OK
    
class MeResource(Resource):
    @jwt_required(fresh=False)
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        data = user_schema.dump(user)
    
        return data, HTTPStatus.OK
    
class UserRecipeListResource(Resource):
    @jwt_required(optional=True, fresh=False)
    @use_args({
        'visibility': fields.Str(missing='public', validate=validate.OneOf(['public', 'private', 'all']))
    }, location='query')
    def get(self, args, username):

        visibility = args.get('visibility')

        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'
        
        recipes = Recipe.get_all_by_user(user_id=user.id, visibility=visibility)

        return recipe_list_schema.dump(recipes), HTTPStatus.OK

class UserAvatarResource(Resource):
    @jwt_required()
    def post(self):
        if 'avatar' not in request.files:
            return {'message': 'Not a valid image'}, HTTPStatus.BAD_REQUEST

        avatar = request.files['avatar']
        
        # accessing file metadata
        filename = avatar.filename
        content_type = avatar.content_type
        content_length = avatar.content_length

        if content_type not in ['image/jpeg', 'image/png']:
            return {'message': 'Only JPEG and PNG images are allowed'}, HTTPStatus.BAD_REQUEST 
        
        user = User.get_by_id(id=get_jwt_identity())
        
        print(f'filename: {filename}')
        print(f'content_type: {content_type}')
        print(f'content_length: {content_length}')

        upload_file(file=avatar, object_name=f'avatars/{filename}')

        return {}, HTTPStatus.OK