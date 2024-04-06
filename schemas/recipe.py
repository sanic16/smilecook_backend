from marshmallow import Schema, fields, post_dump, validate, ValidationError, validates
from schemas.user import UserSchema
from utils import generate_presigned_url

def validate_num_of_servings(n):
        if n < 1:
            raise ValidationError('Number of servings must be greater than 0.')
        if n > 50:
            raise ValidationError('Number of servings must not be greater than 50.')
        
class RecipeSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(validate=[validate.Length(max=200)], required=True)
    directions = fields.List(fields.String(), required=True)
    ingredients = fields.List(fields.String(), required=True)
    num_of_servings = fields.Integer(validate=validate_num_of_servings)
    cook_time = fields.Integer()
    is_publish = fields.Boolean(dump_only=True)
    cover_image = fields.Method(serialize='get_recipe_cover_url')
    popularity = fields.Integer(dump_only=True)

    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('cook_time')
    def validate_cook_time(self, value):
         if value < 1:
              raise ValidationError('Cook time must be greater than 0.')
         if value > 300:
              raise ValidationError('Cook time must not be greater than 300.')
     
    def get_recipe_cover_url(self, recipe):
         
          if recipe.cover_image:
               return generate_presigned_url(recipe.cover_image)
          else:
               return generate_presigned_url('uploads_cover_image/default.jpg')
          
    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
         if many:
              return {'data': data}
         return data    

     



    
        
