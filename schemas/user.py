from marshmallow import Schema, fields
from utils import hash_password, generate_presigned_url

class UserSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.Method(required=True, deserialize='load_password')
    bio = fields.String()
    is_active = fields.Boolean(dump_only=True)
    is_admin = fields.Boolean(dump_only=True)
    avatar_url = fields.Method(serialize='get_avatar_url')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def load_password(self, value):
        return hash_password(value)
    
    def get_avatar_url(self, user):
        print(user.avatar_image)
        if user.avatar_image:
            return generate_presigned_url(user.avatar_image)
        else:
            return None