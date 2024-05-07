import boto3
import json
from botocore.exceptions import ClientError

class S3Utilities:
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def print_all_s3_buckets(self):
        try:
            s3_resource = boto3.resource('s3')
            print("List of buckets:")
            for bucket in s3_resource.buckets.all():
                print("\t", bucket.name)
            return True
        except ClientError as e:
            print(f"Failed to list S3 buckets: {e}")
            return False
    
    def create_bucket(self, bucket_name, region=None):
        try:
            if region is None:
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': region}
                self.s3_client.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
            print(f"Bucket '{bucket_name}' created successfully.")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'BucketAlreadyOwnedByYou':
                print(f"Bucket '{bucket_name}' already exists.")
                return True
            else:
                print(f"Failed to create bucket '{bucket_name}': {e}")
                return False

    def set_policy(self, bucket_name, bucket_policy):
        try:
            bucket_policy_json = json.dumps(bucket_policy)
            self.s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_json)
            print(f"Policy set successfully for bucket '{bucket_name}'")
            return True
        except ClientError as e:
            print(f"Failed to set policy for bucket '{bucket_name}': {e}")
            return False

    def get_policy(self, bucket_name):
        try:
            result = self.s3_client.get_bucket_policy(Bucket=bucket_name)
            return result['Policy']
        except ClientError as e:
            print(f"Failed to retrieve policy for bucket '{bucket_name}': {e}")
            return None

    def delete_policy(self, bucket_name):
        try:
            self.s3_client.delete_bucket_policy(Bucket=bucket_name)
            print(f"Policy deleted successfully for bucket '{bucket_name}'")
            return True
        except ClientError as e:
            print(f"Failed to delete policy for bucket '{bucket_name}': {e}")
            return False

    def download_file(self, bucket, object_name, file_name):
        try:
            self.s3_client.download_file(bucket, object_name, file_name)
            print(f"File '{file_name}' uploaded successfully to bucket '{bucket}' as '{object_name}'")
            return True
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
            return False
        except ClientError as e:
            print(f"Failed to upload file '{file_name}' to bucket '{bucket}': {e}")
            return False

    def upload_file(self, bucket, file_name, object_name):
        try:
            self.s3_client.upload_file(file_name, bucket, object_name)
            print(f"File '{file_name}' uploaded successfully to bucket '{bucket}' as '{object_name}'")
            return True
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
            return False
        except ClientError as e:
            print(f"Failed to upload file '{file_name}' to bucket '{bucket}': {e}")
            return False
