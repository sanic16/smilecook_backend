from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.recipe import Recipe, recipe_list

class RecipeListResource(Resource):
    def get(self):
        data = []

        for recipe in recipe_list:
            if recipe.is_publish:
                data.append(recipe.data)

        return {'data': data}, HTTPStatus.OK
    
    def post(self):
        data = request.get_json()
        recipe = Recipe(
            name=data.get('name'),
            description=data.get('description'),
            num_of_servings=data.get('num_of_servings'),
            cook_time=data.get('cook_time'),
            directions=data.get('directions'),
            ingredients=data.get('ingredients')
        )

        recipe_list.append(recipe)

        return recipe.data, HTTPStatus.CREATED
    
class RecipeResource(Resource):
    def get(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id and recipe.is_publish), None)
    
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        return recipe.data, HTTPStatus.OK

    def put(self, recipe_id):
        data = request.get_json()
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        recipe.name = data.get('name')
        recipe.description = data.get('description')
        recipe.num_of_servings = data.get('num_of_servings')
        recipe.cook_time = data.get('cook_time')
        recipe.directions = data.get('directions')
        recipe.ingredients = data.get('ingredients')

        return recipe.data, HTTPStatus.OK
    
    def delete(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        recipe_list.remove(recipe)

        return {}, HTTPStatus.NO_CONTENT

class RecipePublishResource(Resource):
    def put(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        recipe.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        recipe.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
    
