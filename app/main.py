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
    # Check required environment variables
    required_vars = ["DOCKER_HUB_LINK", "GITHUB_PROJECT_LINK", "AWS_ACCESS_KEY_ID", 
                    "AWS_SECRET_ACCESS_KEY", "AWS_REGION", "CODE_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        return {
            "status": "unhealthy",
            "container": os.getenv("DOCKER_HUB_LINK", "not_set"),
            "project": os.getenv("GITHUB_PROJECT_LINK", "not_set"),
            "error": f"Missing environment variables: {', '.join(missing_vars)}"
        }
    
    # Check DynamoDB connection
    try:
        # Try to get the secret code to verify DynamoDB connection
        code_name = os.getenv("CODE_NAME")
        dynamodb_client.get_secret_code(code_name)
    except Exception as e:
        return {
            "status": "unhealthy",
            "container": os.getenv("DOCKER_HUB_LINK", "not_set"),
            "project": os.getenv("GITHUB_PROJECT_LINK", "not_set"),
            "error": f"DynamoDB connection failed: {str(e)}"
        }
    
    # All checks passed
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
