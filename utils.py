import boto3
from passlib.hash import pbkdf2_sha256
import os
import uuid

BUCKET_NAME = os.environ.get('BUCKET_NAME')

def hash_password(password):
    return pbkdf2_sha256.hash(password)

def check_password(password, hashed):
    return pbkdf2_sha256.verify(password, hashed)

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1'
) 

def generate_presigned_url(operation, object_key=None, expiration=30, resource='user'):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name='us-east-1'
    )
    BUCKET_NAME = 'flask-react-gt-aws-bucket'


    if(operation == 'delete_and_upload'):
        try:
            res = s3_client.delete_object(Bucket=BUCKET_NAME, Key=object_key)
           
        except Exception as e:
           
            return False
        
    if resource == 'user':
        new_object_key = f'uploads_avatar/{uuid.uuid4()}.jpeg' 
    elif resource == 'recipe':
        new_object_key = f'uploads_cover_image/{uuid.uuid4()}.jpeg'

 
    try:
        response = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': new_object_key,
                'ContentType': 'image/jpeg'
            },
            HttpMethod='PUT',
            ExpiresIn=expiration
        )
    except Exception as e:
        return False
    
    
    return  new_object_key, response


def get_object_url(bucket_name, object_key):
    return f'https://{bucket_name}.s3.amazonaws.com/{object_key}'
