import json
import boto3
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client('s3')
bucket_name = os.environ.get('S3_BUCKETNAME')
filename = os.environ.get('S3_FILENAME')


def lambda_handler(event, context):

    json_data = json.loads(event['body'])

    uploadByteStream = bytes(json.dumps(
        json_data['data']['metrics']).encode('UTF-8'))
    s3.put_object(Bucket=bucket_name, Key=filename, Body=uploadByteStream)

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
