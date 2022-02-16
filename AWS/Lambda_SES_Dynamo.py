import json
import urllib.parse
import datetime
# pytz requires an layer setup in lambda
import pytz
import boto3
from boto3.dynamodb.conditions import Key, Attr


s3 = boto3.client('s3')
ses = boto3.client('ses')

# Must specify timezone since the server hosting lambda could be in east coast, which will roll to the next day
Current_Time = datetime.datetime.now(tz=pytz.timezone('Canada/Mountain'))
Current_Date = str(Current_Time.date())




def lambda_handler(event, context):
    
    # Gather bucket name and file name(key) from s3 events. 

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('calgary_re')
    
    try:
        
        #record_date is the partition key,using query instead of scan to save the cost
        Dynamo_Response = table.query(
        KeyConditionExpression=Key('record_date').eq(f'{Current_Date}') 
        )


        items = Dynamo_Response['Items']
        # use SES later on to notify user how many records are uploaded and a few samples for assurance.
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
