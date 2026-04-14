from flask import Flask, jsonify
import boto3

app = Flask(__name__)

# S3 client (LocalStack - Kubernetes service name)
s3 = boto3.client(
    's3',
    endpoint_url='http://localstack:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

@app.get('/user')
def get_user():
    return jsonify({
        "message": "User Service is Running",
        "user": "Admin"
    })

@app.get('/upload')
def upload_to_s3():
    bucket_name = 'my-devops-project-bucket'
    file_name = 'test-file.txt'
    content = 'Bhai, container se S3 mein file aa gayi!'

    try:
        # ✅ bucket exist check
        try:
            s3.head_bucket(Bucket=bucket_name)
        except:
            # ✅ agar nahi hai to create kar
            s3.create_bucket(Bucket=bucket_name)

        # ✅ file upload
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=content)

        return jsonify({
            "status": "Success",
            "message": f"{file_name} uploaded to {bucket_name}"
        })

    except Exception as e:
        return jsonify({
            "status": "Error",
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)