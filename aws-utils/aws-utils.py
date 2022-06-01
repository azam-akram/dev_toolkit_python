from fileinput import filename
import boto3
import json
from datetime import datetime
import requests

endpoint = "https://test.com/v1/task"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer my-test-jwt-token",
}

def copyFileToS3Bucket():
    s3 = boto3.resource('s3')

    file_name = 'my-image.jpeg'

    source_bucket = {
        'Bucket': 'my-source-s3-bucket',
        'Key': 'dev/source-files/' + file_name
    }

    target_bucket = s3.Bucket('my-target-s3-bucket')
    targetKey = 'dev/received-files/'+ file_name
  
    target_bucket.copy(source_bucket, targetKey)

    print ("Copied  file completd")


def publishEventOnSNSTopic():
    file_name = 'my-image.jpeg'
    targetKey = 'dev/received-files/'+ file_name

    event = {
        "eventVersion": "2.1",
        "eventSource": "aws:s3",
        "awsRegion": "eu-west-1",
        "eventTime": "2019-10-18T13:09:21.726Z",
        "eventName": "ObjectCreated:Put",
        "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "7399b1c9-bbe9-4ca9-bdda-a02216187222",
        "bucket": {
            "name": "my-target-s3-bucket",
            "ownerIdentity": {
            "principalId": "APXU1GD6WTEYH"
            },
            "arn": "arn:aws:s3:::my-target-s3-bucket"
        },
        "object": {
            "key": targetKey
        }
        }
    }
    
    client = boto3.client('sns')
    response = client.publish(
        TargetArn = "arn:aws:sns:eu-west-1:m-target-sns-topic",
        Message=json.dumps({'default': json.dumps(event)}),
        MessageStructure='json'
    )
  
    print(response)

def post_http_request():
    payload = {
        "id": 1,
        "deadline": "2022-12-31T00:00:00Z",
        "priority": "high"
    }

    print(requests.post(endpoint, data=json.dumps(payload), headers=headers).json())


def aws_utils():
    copyFileToS3Bucket()
    
    publishEventOnSNSTopic()

    post_http_request()
    
aws_utils()