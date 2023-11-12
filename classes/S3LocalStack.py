import boto3
from botocore.session import Session

class S3LocalStack:
    def __init__(self,
                 aws_config_file,
                 aws_shared_credentials_file,
                 localstack_endpoint_url,
                 aws_region):
        
        # AWS credentials.
        self.aws_config_file = aws_config_file
        self.aws_shared_credentials_file = aws_shared_credentials_file
        
        # AWS region
        self.aws_region = aws_region
        
        # Localstack endpoint url.
        self.localstack_endpoint_url = localstack_endpoint_url
        
        # Create S3 client.
        self.s3_client = self.create_client()
    
    def create_client(self, profile='localstack'):
        """
        Creates an S3 client using the provided profile and returns it.

        Args:
            profile (str): The name of the profile to use. Defaults to 'localstack'.

        Returns:
            boto3.client: An S3 client object.
        """
        # Load credentials
        session = Session(profile=profile)
        credentials = session.get_credentials()

        # Create S3 client
        s3_client = boto3.client('s3', 
                                 region_name=self.aws_region,
                                 endpoint_url=self.localstack_endpoint_url, 
                                 aws_access_key_id=credentials.access_key, 
                                 aws_secret_access_key=credentials.secret_key)
        return s3_client
    
    def create_bucket(self, bucket_name):
        """
        Crea un nuevo bucket en Amazon S3 pasado como parámetro.

        Args:
            bucket_name (str): El nombre del bucket a crear.

        Returns:
            None
        """
        self.s3_client.create_bucket(Bucket=bucket_name)
        print('Bucket ' + bucket_name + ' created')
        
    def initialize_bucket(self, bucket_name, files):
        """
        Sube las imágenes especificadas al bucket de S3 pasado como parámetro.

        Args:
            bucket_name (str): El nombre del bucket de S3 al que se subirán las imágenes.
            images (list): Una lista de nombres de archivo de imágenes que se subirán al bucket.

        Returns:
            None
        """
        for file in files: 
            self.s3_client.upload_file('images/' + file, bucket_name, file)
    
    def list_bucket_objects(self, bucket_name):
        """
        Lista todos los objetos del bucket pasado como parámetro.

        Args:
            bucket_name (str): El nombre del bucket de S3 del que se listarán los objetos.

        Returns:
            None
        """
        response = self.s3_client.list_objects_v2(Bucket=bucket_name)
        for object in response['Contents']:
            print(object['Key'])
    
    def truncate_bucket(self, bucket_name, delete_bucket=False):
        """
        Elimina todos los objetos del bucket pasado como parámetro.

        Args:
            bucket_name (str): El nombre del bucket de S3 del que se eliminarán los objetos.
            delete_bucket (bool): Si es True, elimina el bucket después de eliminar los objetos. Defaults to False.

        Returns:
            None
        """
        response = self.s3_client.list_objects_v2(Bucket=bucket_name)
        # check if response is not empty
        if 'Contents' not in response:
            print('Bucket ' + bucket_name + ' is empty')
        else:
            for object in response['Contents']:
                self.s3_client.delete_object(Bucket=bucket_name, Key=object['Key'])
                print('Deleted object: ' + object['Key'])
        if delete_bucket:
            self.s3_client.delete_bucket(Bucket=bucket_name)
            print('Bucket ' + bucket_name + ' deleted')
    
    def list_buckets(self):
        """
        Lista todos los buckets de S3.

        Returns:
            None
        """
        response = self.s3_client.list_buckets()
        for bucket in response['Buckets']:
            print(bucket['Name'])
    
    def copy_objects(self, source_bucket_name, destination_bucket_name):
        """
        Copia todos los objetos del bucket source al bucket destination.

        Args:
            source_bucket_name (str): El nombre del bucket de S3 del que se copiarán los objetos.
            destination_bucket_name (str): El nombre del bucket de S3 al que se copiarán los objetos.

        Returns:
            None
        """
        response = self.s3_client.list_objects_v2(Bucket=source_bucket_name)
        for object in response['Contents']:
            self.s3_client.copy_object(Bucket=destination_bucket_name, 
                                       CopySource={'Bucket': source_bucket_name, 'Key': object['Key']}, 
                                       Key=object['Key'])
            print('Copied object ' + object['Key'] + ' from bucket ' + source_bucket_name + ' to bucket ' + destination_bucket_name)
