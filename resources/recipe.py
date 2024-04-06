from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.recipe import Recipe
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.recipe import RecipeSchema
from marshmallow import ValidationError
from utils import generate_update_presigned_url, delete_object

recipe_schema = RecipeSchema()
recipe_list_schema = RecipeSchema(many=True)

class RecipeListResource(Resource):
    def get(self):
        recipes = Recipe.get_all_published()
             
        return recipe_list_schema.dump(recipes), HTTPStatus.OK
    
    @jwt_required()
    def post(self):
        data = request.get_json()

        current_user = get_jwt_identity()

        try:
            data = recipe_schema.load(data=data)
        except ValidationError as error:
            return {'message': 'Validation error', 'errors': error.messages}, HTTPStatus.BAD_REQUEST

        recipe = Recipe(**data)
        recipe.user_id = current_user         
        recipe.save()

        return {'id': recipe.id}, HTTPStatus.CREATED


class RecipeResource(Resource):
    @jwt_required(optional=True, fresh=False)
    def get(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if recipe.is_publish == False and recipe.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return recipe_schema.dump(recipe), HTTPStatus.OK
     
        
    @jwt_required()
    def put(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        data = request.get_json()

        recipe.name = data.get('name', recipe.name)
        recipe.description = data.get('description', recipe.description)
        recipe.num_of_servings = data.get('num_of_servings', recipe.num_of_servings)
        recipe.cook_time = data.get('cook_time', recipe.cook_time)
        recipe.directions = data.get('directions', recipe.directions)
        recipe.ingredients = data.get('ingredients', recipe.ingredients)

        recipe.save()

        return recipe.data(), HTTPStatus.OK
    
    @jwt_required()
    def patch(self, recipe_id):
        data = request.get_json()
        try:
            data = recipe_schema.load(data=data, partial=('name', 'directions', 'ingredients', 'description'))
        except ValidationError as error:
            return {'message': 'Validation error', 'errors': error.messages}, HTTPStatus.BAD_REQUEST
        
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        recipe.name = data.get('name', recipe.name)
        recipe.description = data.get('description', recipe.description)
        recipe.num_of_servings = data.get('num_of_servings', recipe.num_of_servings)
        recipe.cook_time = data.get('cook_time', recipe.cook_time)
        recipe.directions = data.get('directions', recipe.directions)
        recipe.ingredients = data.get('ingredients', recipe.ingredients)

        recipe.save()

        return recipe_schema.dump(recipe), HTTPStatus.OK
    
    
    @jwt_required()    
    def delete(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        recipe.delete()

        return {}, HTTPStatus.NO_CONTENT

class RecipePublishResource(Resource):

    @jwt_required()
    def put(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if(current_user != recipe.user_id):
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        recipe.is_publish= True
        recipe.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required()
    def delete(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if(current_user != recipe.user_id):
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        recipe.is_publish = False
        recipe.save()

        return {}, HTTPStatus.NO_CONTENT

class RecipeCoverResource(Resource):

    @jwt_required()
    def put(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if(recipe.cover_image):
            delete_object(object_key=recipe.cover_image)
            recipe.cover_image = None
            recipe.save()
            aws = generate_update_presigned_url(resource='recipe', expiration=60)
            if not aws:
                return {'message': 'Error generating presigned URL'}, HTTPStatus.INTERNAL_SERVER_ERROR
            
            recipe.cover_image_temporary = aws[0]
            recipe.save()
            return {'presigned_url': aws[1]}, HTTPStatus.OK
        else:
            aws = generate_update_presigned_url(resource='recipe', expiration=60)
            if not aws:
                return {'message': 'Error generating presigned URL'}, HTTPStatus.INTERNAL_SERVER_ERROR
            recipe.cover_image_temporary = aws[0]
            recipe.save()
            return {'presigned_url': aws[1]}, HTTPStatus.OK
    
    @jwt_required()
    def post(self, recipe_id):        
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        recipe.cover_image = recipe.cover_image_temporary
        recipe.cover_image_temporary = None
        recipe.save()
        
        return {}, HTTPStatus.NO_CONTENT
    
