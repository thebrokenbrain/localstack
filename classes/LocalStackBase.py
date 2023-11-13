import boto3
from botocore.session import Session

class LocalStackBase:
    def __init__(self,
                 aws_config_file,
                 aws_shared_credentials_file,
                 localstack_endpoint_url,
                 aws_region,
                 service_name):
        
        # AWS credentials.
        self.aws_config_file = aws_config_file
        self.aws_shared_credentials_file = aws_shared_credentials_file
        
        # AWS region
        self.aws_region = aws_region
        
        # Localstack endpoint url.
        self.localstack_endpoint_url = localstack_endpoint_url
        
        # Create client.
        self.client = self.create_client(service_name)
    
    def create_client(self, service_name, profile='localstack'):
        # Load credentials
        session = Session(profile=profile)
        credentials = session.get_credentials()

        # Create client
        client = boto3.client(service_name,
                              region_name=self.aws_region,
                              endpoint_url=self.localstack_endpoint_url, 
                              aws_access_key_id=credentials.access_key, 
                              aws_secret_access_key=credentials.secret_key)
        return client