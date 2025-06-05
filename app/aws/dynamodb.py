import os
import boto3
from botocore.exceptions import ClientError
from typing import Optional

class DynamoDBClient:
    def __init__(self):
        self.client = boto3.client(
            'dynamodb',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.table_name = 'devops-challenge'

    def get_secret_code(self, code_name: str) -> Optional[str]:
        try:
            response = self.client.get_item(
                TableName=self.table_name,
                Key={
                    'code_name': {'S': code_name}
                }
            )
            
            if 'Item' in response:
                return response['Item'].get('secret_code', {}).get('S')
            return None
            
        except ClientError as e:
            print(f"Error accessing DynamoDB: {e}")
            return None 