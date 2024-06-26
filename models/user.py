from extensions import db
from datetime import datetime
import pytz

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200))
    is_active = db.Column(db.Boolean(), default=False)
    is_admin = db.Column(db.Boolean(), default=False)
    bio = db.Column(db.Text)
    avatar_temporary = db.Column(db.String(150), default=None)
    avatar_image = db.Column(db.String(150), default=None)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')))
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')), onupdate=datetime.now(pytz.timezone('America/Guatemala')))

    recipes = db.relationship('Recipe', backref='user')

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()


    