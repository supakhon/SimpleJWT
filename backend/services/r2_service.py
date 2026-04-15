import boto3
import os
# import uuid

from dotenv import load_dotenv
load_dotenv() # Load .env file into os.environ

# s3 - Amazon's ...bruh
s3 = boto3.client(
    's3',
    # endpoint_url='https://<account_id>.r2.cloudflarestorage.com',
    endpoint_url = os.environ.get("R2_URL"),
    aws_access_key_id = os.environ.get("R2_ACCESS_KEY_ID"),
    aws_secret_access_key = os.environ.get("R2_SECRET_ACCESS_KEY")
)

domain_url = os.environ.get('DOMAIN_URL')

def upload_file(local_path, bucket, key):
    s3.upload_file( local_path, bucket, key )
    return f"This is file url: {domain_url}{bucket}{key}"

# local = './0f60a564de9d25e027af0a929e655320.jpg'
# bucket = 'Text'
# # filename = f"{uuid.uuid4()}.txt"
# # key = f"{filename}"
# key = '0f60a564de9d25e027af0a929e655320.jpg'


# s3.upload_file(
#     local,
#     bucket,
#     key
# )

# print(f'{os.environ.get("DOMAIN_URL")}{bucket}/{key}')

