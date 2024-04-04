from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.recipe import Recipe
from flask_jwt_extended import jwt_required, get_jwt_identity

class RecipeListResource(Resource):
    def get(self):
        recipes = Recipe.get_all_published()

        data = []
        for recipe in recipes:
            data.append(recipe.data())
        
        return {'data': data}, HTTPStatus.OK
    
    @jwt_required()
    def post(self):
        data = request.get_json()

        current_user = get_jwt_identity()
        recipe = Recipe(
            name = data.get('name'),
            description = data.get('description'),
            num_of_servings = data.get('num_of_servings'),
            cook_time = data.get('cook_time'),
            directions = data.get('directions'),
            ingredients = data.get('ingredients'),
            user_id = current_user
,        )
        
        recipe.save()

        return recipe.data(), HTTPStatus.CREATED


class RecipeResource(Resource):
    @jwt_required(optional=True, fresh=False)
    def get(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if recipe.is_publish == False and recipe.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return recipe.data(), HTTPStatus.OK
     
        
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

    
