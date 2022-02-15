import json
import urllib.parse
import datetime
import pytz
import boto3
from boto3.dynamodb.conditions import Key, Attr


s3 = boto3.client('s3')
ses = boto3.client('ses')

Current_Time = datetime.datetime.now(tz=pytz.timezone('Canada/Mountain'))
Current_Date = str(Current_Time.date())




def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('calgary_re')
    
    try:
        
        Dynamo_Response = table.query(
        KeyConditionExpression=Key('record_date').eq(f'{Current_Date}') 
        )


        items = Dynamo_Response['Items']
        item_count = len(items)
        top_10 = items[:10]
            


        response_ses = ses.send_email(
            Source='yukimister87@gmail.com',
            Destination={
                'ToAddresses': [
                    'moonmana@gmail.com',
                ]
            },
            Message={
                'Subject': {
                    'Data': 'New Files in S3 ',
                    
                },
                'Body': {
                    'Text': {
                        'Data': f'File Name: {key}  \nBucket Name: {bucket} \n\n    Total number of record uploaded: {item_count} \n\n    Sample:\n\n      {top_10}' 
                        
                    }

                        
                    
                }
            }
        )
        
        return  
        
    except Exception as e:
        print(e)
