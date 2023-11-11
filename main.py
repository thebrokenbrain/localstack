import boto3
from botocore.session import Session
from dotenv import load_dotenv
import os    

# Load .env file
load_dotenv()

# Get AWS credentials from .env file
aws_config_file = os.getenv("AWS_CONFIG_FILE")
aws_shared_credentials_file = os.getenv("AWS_SHARED_CREDENTIALS_FILE")

# Get endpoint url from .env file
localstack_endpoint_url = os.getenv("LOCALSTACK_ENDPOINT_URL")

# Specify the AWS region
aws_region = 'us-east-1'  # replace with your region

# Create s3 client.
def create_s3_client():
    # Load credentials
    session = Session(profile='localstack')
    credentials = session.get_credentials()

    # Create S3 client
    s3_client = boto3.client('s3', 
                             region_name=aws_region,
                             endpoint_url=localstack_endpoint_url, 
                             aws_access_key_id=credentials.access_key, 
                             aws_secret_access_key=credentials.secret_key)
    return s3_client

# Create a bucket.
def create_bucket(bucket_name):
    s3_client = create_s3_client()
    s3_client.create_bucket(Bucket=bucket_name)

# List all objects of a bucket.
def list_bucket_objects(bucket_name):
    s3_client = create_s3_client()
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    for object in response['Contents']:
        print(object['Key'])

# Initialize bucket with images.
def initialize_bucket(bucket_name, images):
    s3_client = create_s3_client()
    for image in images:
        s3_client.upload_file('images/' + image, bucket_name, image)

# Copy all objects from one bucket to another.
def copy_objects(source_bucket_name, destination_bucket_name):
    s3_client = create_s3_client()
    response = s3_client.list_objects_v2(Bucket=source_bucket_name)
    for object in response['Contents']:
        s3_client.copy_object(Bucket=destination_bucket_name, 
                              CopySource={'Bucket': source_bucket_name, 'Key': object['Key']}, 
                              Key=object['Key'])
        print('Copied object: ' + object['Key'])
        
# Delete all objects in a bucket and print the objects deleted.
def delete_all_objects(bucket_name):
    s3_client = create_s3_client()
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    for object in response['Contents']:
        s3_client.delete_object(Bucket=bucket_name, Key=object['Key'])
        print('Deleted object: ' + object['Key'])

# Delete a bucket.
def delete_bucket(bucket_name):
    s3_client = create_s3_client()
    s3_client.delete_bucket(Bucket=bucket_name)
    print('Bucket deleted')
            
if __name__ == '__main__':
    # Create bucket-1 and bucket-2
    create_bucket('bucket-1')
    create_bucket('bucket-2')
    
    # Initialize bucket-1 with images    
    print('Initializing bucket-1 with images...')
    images = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg']
    initialize_bucket('bucket-1', images)
    list_bucket_objects('bucket-1')
    
    # Initialize bucket-2 with images
    print('\nInitializing bucket-2 with images...')
    images = ['6.jpg', '7.jpg', '8.jpg', '9.jpg', '10.jpg']
    initialize_bucket('bucket-2', images)
    list_bucket_objects('bucket-2')
    
    # Copy all objects from bucket-1 to bucket-2
    print('\nCopying all objects from bucket-1 to bucket-2...')
    copy_objects('bucket-1', 'bucket-2')
    
    # List objects of bucket-2
    print('\nListing objects of bucket-2...')
    list_bucket_objects('bucket-2')
        
    # Delete bucket-1
    print('\nDeleting bucket-1...')
    delete_all_objects('bucket-1')
    delete_bucket('bucket-1')
    
    # Delete bucket-2
    print('\nDeleting bucket-2...')
    delete_all_objects('bucket-2')
    delete_bucket('bucket-2')
    