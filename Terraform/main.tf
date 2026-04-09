provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true # Ye line zaroori hai error hatane ke liye

  endpoints {
    s3  = "http://host.docker.internal:4566"
    sts = "http://localhost:4566" # STS bhi localstack pe bhej do
  }
}

resource "aws_s3_bucket" "user_data" {
  bucket = "my-devops-project-bucket"
} 
