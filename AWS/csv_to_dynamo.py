import datetime
import pytz
import csv
import boto3
from botocore.exceptions import ClientError


Current_Time = datetime.datetime.now(tz=pytz.timezone('Canada/Mountain'))
Current_Date = Current_Time.date()
File_Name = str(Current_Date)

dynamodb = boto3.resource('dynamodb')

try:
    # Use csv DictReader to grab each row and batchwrite to DynamoDB as document
    with open(f'{File_Name}.csv', newline='') as csvfile:


        table = dynamodb.Table('calgary_re')

        with table.batch_writer() as batch:

            rows = csv.DictReader(csvfile, delimiter = '\t')
            for row in rows:
                batch.put_item(
                        Item={

                            'record_date': row['record_date'],
                            'years_built': row['years_built'],
                            'addr': row['addr'],
                            'community': row['community'],                          
                            'beds': row['beds'],
                            'baths': row['baths'],
                            'floor_space': row['floor_space'],
                            'land_size': row['land_size'],
                            'last_sold': row['last_sold'],
                            'last_sold_date': row['last_sold_date'],
                            'city_appraisal': row['city_appraisal'],
                            'link': row['link']
                        }
                )
        print('csv uploaded!')


except Exception as e:
    print(e)


def upload_file(file_name, bucket, object_name=None):


    if object_name is None:
        object_name = file_name


    s3_client = boto3.client('s3')

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print('File upload successful!')

    except ClientError as e:
        print(e)


upload_file(f'{File_Name}.csv', 'csv-drop-box')

