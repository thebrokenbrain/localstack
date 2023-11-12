from classes.S3LocalStack import S3LocalStack
from dotenv import load_dotenv
import os  

if __name__ == '__main__':
    # Load .env file where the AWS credentials variables are stored.
    load_dotenv()
    
    # Se crea el objeto S3LocalStack.
    s3 = S3LocalStack(os.getenv("AWS_CONFIG_FILE"),
                    os.getenv("AWS_SHARED_CREDENTIALS_FILE"),
                    os.getenv("LOCALSTACK_ENDPOINT_URL"),
                    'us-east-1')

    # Se crean los buckets.
    print('Creating buckets')
    s3.create_bucket('bucket-1')
    s3.create_bucket('bucket-2')

    # Se suben objetos al bucket-1.
    print('\nInitializing bucket-1')
    s3.initialize_bucket('bucket-1', 
                        ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg'])
    s3.list_bucket_objects('bucket-1')

    # Se suben objetos al bucket-2.
    print('\nInitializing bucket-2')
    s3.initialize_bucket('bucket-2', 
                        ['6.jpg', '7.jpg', '8.jpg', '9.jpg'])
    s3.list_bucket_objects('bucket-2')

    # Se copian los objetos del bucket-1 al bucket-2.
    print('\nCopying objects from bucket-1 to bucket-2')
    s3.copy_objects('bucket-1', 'bucket-2')
    print('\nObjects in bucket-2 after copy objects from bucket-1')
    s3.list_bucket_objects('bucket-2')

    # Se eliminan los buckets.
    print ('\nDeleting buckets')
    s3.truncate_bucket('bucket-1', delete_bucket=True)
    s3.truncate_bucket('bucket-2', delete_bucket=True)