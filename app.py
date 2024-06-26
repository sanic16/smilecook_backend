from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, send_from_directory  
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS 
from config import Config
from extensions import db, jwt

from resources.recipe import (RecipeListResource, RecipeResource, RecipePublishResource,
                              RecipeCoverResource)
from resources.user import (UserListResource, UserResource, MeResource, UserRecipeListResource, 
                            UserAvatarResource, MeRecipeListResource)

from resources.token import TokenResource, RefreshResource, RevokeResource

from models.token import TokenBlocklist

def create_app():
    app = Flask(__name__, static_folder='client/assets')
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    return app

def register_extensions(app):
    db.init_app(app=app)
    jwt.init_app(app=app)
    cors = CORS(app=app, resources={r"/*": {"origins": "*"}})
    migrate = Migrate(app=app, db=db)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload['jti']
        token = TokenBlocklist.query.filter_by(jti=jti).scalar()

        return token is not None


def register_resources(app):
    api = Api(app=app)
    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')

    api.add_resource(UserListResource, '/users')
    api.add_resource(UserAvatarResource, '/users/avatar')    
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')
    api.add_resource(MeRecipeListResource, '/me/recipes')
    api.add_resource(UserRecipeListResource, '/users/<string:username>/recipes')
    api.add_resource(RecipeCoverResource, '/recipes/<int:recipe_id>/cover')

    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')

app = create_app()

@app.errorhandler(404)
def not_found(e):
    return serve()
@app.route('/')
def serve():
    return send_from_directory('client', 'index.html')

if __name__ == '__main__':
    app.run(port=os.environ.get('PORT') or 5000)

