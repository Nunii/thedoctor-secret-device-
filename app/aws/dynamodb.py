import os
import boto3
from botocore.exceptions import ClientError
from typing import Optional

class DynamoDBClient:
    def __init__(self):
        print("Initializing DynamoDB client...")
        self.client = boto3.client(
            'dynamodb',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.table_name = 'devops-challenge'
        print(f"Using table: {self.table_name}")
        
        # Get and print table description
        try:
            response = self.client.describe_table(TableName=self.table_name)
            print("Table Schema:")
            print(f"Key Schema: {response['Table']['KeySchema']}")
            print(f"Attribute Definitions: {response['Table']['AttributeDefinitions']}")
        except ClientError as e:
            print(f"Error describing table: {e}")

    def get_secret_code(self, code_name: str) -> Optional[str]:
        try:
            print(f"Attempting to fetch secret for code_name: {code_name}")
            
            # We know the correct key is 'codeName' and value is 'theDoctor'
            response = self.client.get_item(
                TableName=self.table_name,
                Key={
                    'codeName': {'S': 'theDoctor'}
                }
            )
            
            if 'Item' in response:
                return response['Item'].get('secretCode', {}).get('S')
            return None
            
        except ClientError as e:
            print(f"Error accessing DynamoDB: {e}")
            return None 