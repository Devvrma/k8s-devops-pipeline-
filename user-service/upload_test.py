import boto3

# LocalStack se connect karne ke liye settings
s3 = boto3.client(
    's3',
    endpoint_url='http://host.docker.internal:4566', # LocalStack ka address
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

# Ek dummy file upload karke check karte hain
bucket_name = 'my-devops-project-bucket'
file_name = 'hello.txt'
content = 'Bhai, DevOps seekh raha hoon maza aa raha hai!'

try:
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=content)
    print(f"Success! {file_name} upload ho gayi bucket mein.")
except Exception as e:
    print(f"Error aa gaya: {e}")