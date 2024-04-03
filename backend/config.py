import os
from datetime import timedelta

db = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME')
}

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    

    