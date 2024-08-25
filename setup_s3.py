import boto3
import os

# AWS credentials and region
AWS_ACCESS_KEY_ID     = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
AWS_REGION = 'us-east-1'

# Initialize S3 client
s3 = boto3.client('s3', 
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name=AWS_REGION)

def create_bucket(bucket_name):
    response = s3.create_bucket(
        Bucket=bucket_name
    )
    print(f"Created bucket: {bucket_name}")

if __name__ == "__main__":
    # Define input, stage-1 and output bucket names
    input_bucket_name = 'input'
    stage_1_bucket = 'stage-1'
    output_bucket = 'output'


    # Create S3 buckets
    create_bucket(input_bucket_name)
    create_bucket(stage_1_bucket)
    create_bucket(output_bucket)


