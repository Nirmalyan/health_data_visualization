import pandas as pd
import boto3
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.environ.get('AWS_ACCESS_ID'),
    aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY'),
)
s3 = session.client('s3')
obj = s3.get_object(Bucket='healthify-autoexport', Key='healthrawdata.json')
cwd = os.getcwd()


def normalize_json():
    with BytesIO(obj['Body'].read()) as bio:
        df = pd.read_json(bio)
    explode = df.explode('data')
    normalize = explode['data'].apply(pd.Series)
    final = pd.concat([explode[:], normalize[:]], axis=1)
    final.drop(['data', 'source'], axis=1, inplace=True)
    final.to_csv('normalized.csv')


def cleanup():
    s3.delete_object(Bucket='healthify-autoexport', Key='healthrawdata.json')
    os.remove('')
