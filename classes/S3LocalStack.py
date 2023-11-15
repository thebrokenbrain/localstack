from classes.LocalStackBase import LocalStackBase

class S3LocalStack(LocalStackBase):
    def create_bucket(self, bucket_name):
        """
        Crea un nuevo bucket en Amazon S3 pasado como parámetro.

        Args:
            bucket_name (str): El nombre del bucket a crear.

        Returns:
            None
        """
        self.client.create_bucket(Bucket=bucket_name)
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
            self.client.upload_file('images/' + file, bucket_name, file)
    
    def list_bucket_objects(self, bucket_name):
        """
        Lista todos los objetos del bucket pasado como parámetro.

        Args:
            bucket_name (str): El nombre del bucket de S3 del que se listarán los objetos.

        Returns:
            None
        """
        response = self.client.list_objects_v2(Bucket=bucket_name)
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
        response = self.client.list_objects_v2(Bucket=bucket_name)
        # check if response is not empty
        if 'Contents' not in response:
            print('Bucket ' + bucket_name + ' is empty')
        else:
            for object in response['Contents']:
                self.client.delete_object(Bucket=bucket_name, Key=object['Key'])
                print('Deleted object: ' + object['Key'])
        if delete_bucket:
            self.client.delete_bucket(Bucket=bucket_name)
            print('Bucket ' + bucket_name + ' deleted')
    
    def list_buckets(self):
        """
        Lista todos los buckets de S3.

        Returns:
            None
        """
        response = self.client.list_buckets()
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
        response = self.client.list_objects_v2(Bucket=source_bucket_name)
        for object in response['Contents']:
            self.client.copy_object(Bucket=destination_bucket_name, 
                                       CopySource={'Bucket': source_bucket_name, 'Key': object['Key']}, 
                                       Key=object['Key'])
            print('Copied object ' + object['Key'] + ' from bucket ' + source_bucket_name + ' to bucket ' + destination_bucket_name)
