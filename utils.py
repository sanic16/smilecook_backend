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




def delete_object(object_key, resource='user'):
    print('Debugging')
    try:
        if resource == 'user':
            print(f'uploads_avatar/{object_key}')
            return s3_client.delete_object(
                Bucket=BUCKET_NAME,
                Key=f'{object_key}'
            )
        elif resource == 'recipe':
            return s3_client.delete_object(
                Bucket=BUCKET_NAME,
                Key=f'{object_key}'
            )
        
    except Exception as e:
        print(e)
        return False

def generate_update_presigned_url(resource, expiration=60, content_type='image/jpeg'):
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
                'ContentType': content_type
            },
            HttpMethod='PUT',
            ExpiresIn=expiration
        )
    except Exception as e:
        return False
    
    return  new_object_key, response

def generate_presigned_url(object_key):
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': object_key
            },
            ExpiresIn=3600
        )
    except Exception as e:
        return False

    return response

def get_object_url(bucket_name, object_key):
    return f'https://{bucket_name}.s3.amazonaws.com/{object_key}'
