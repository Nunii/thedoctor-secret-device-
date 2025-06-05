import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from app.aws.dynamodb import DynamoDBClient

# Load environment variables
load_dotenv()

app = FastAPI()
dynamodb_client = DynamoDBClient()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "container": os.getenv("DOCKER_HUB_LINK", "not_set"),
        "project": os.getenv("GITHUB_PROJECT_LINK", "not_set")
    }

@app.get("/secret")
async def get_secret():
    code_name = os.getenv("CODE_NAME")
    if not code_name:
        raise HTTPException(status_code=500, detail="CODE_NAME not configured")
    
    # Debug logging
    print(f"Attempting to fetch secret for code_name: {code_name}")
    print(f"AWS Region: {os.getenv('AWS_REGION')}")
    print(f"AWS Access Key ID exists: {bool(os.getenv('AWS_ACCESS_KEY_ID'))}")
    print(f"AWS Secret Key exists: {bool(os.getenv('AWS_SECRET_ACCESS_KEY'))}")
    
    secret_code = dynamodb_client.get_secret_code(code_name)
    if not secret_code:
        raise HTTPException(status_code=404, detail="Secret code not found")
    
    return {"secret_code": secret_code}
