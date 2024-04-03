from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from extensions import db 

from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource
from resources.user import UserListResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    return app

def register_extensions(app):
    db.init_app(app=app)
    migrate = Migrate(app=app, db=db)

def register_resources(app):
    api = Api(app=app)
    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')

    api.add_resource(UserListResource, '/users')

if __name__ == '__main__':
    app = create_app()
    app.run()

