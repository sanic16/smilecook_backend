import boto3
from passlib.hash import pbkdf2_sha256
import os
from io import BytesIO

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

def generate_presigned_url(object_name, expiration=3600):
    return s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': object_name,
            # 'ContentType': 'Video/mp4'
        },
        HttpMethod='GET',
        ExpiresIn=expiration,        
    )

def upload_file(file, object_name):
    file_stream = BytesIO()
    file.save(file_stream)
    
    return s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=object_name,
        Body=file_stream.getvalue()
    )
