import os
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    with patch.dict(os.environ, {
        "DOCKER_HUB_LINK": "https://hub.docker.com/test",
        "GITHUB_PROJECT_LINK": "https://github.com/test"
    }):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {
            "status": "healthy",
            "container": "https://hub.docker.com/test",
            "project": "https://github.com/test"
        }

def test_secret_endpoint_missing_code_name():
    with patch.dict(os.environ, {}, clear=True):
        resp = client.get("/secret")
        assert resp.status_code == 500
        assert resp.json() == {"detail": "CODE_NAME not configured"}

@patch('app.aws.dynamodb.DynamoDBClient.get_secret_code')
def test_secret_endpoint_success(mock_get_secret):
    mock_get_secret.return_value = "test_secret"
    with patch.dict(os.environ, {"CODE_NAME": "test_code"}):
        resp = client.get("/secret")
        assert resp.status_code == 200
        assert resp.json() == {"secret_code": "test_secret"}

@patch('app.aws.dynamodb.DynamoDBClient.get_secret_code')
def test_secret_endpoint_not_found(mock_get_secret):
    mock_get_secret.return_value = None
    with patch.dict(os.environ, {"CODE_NAME": "test_code"}):
        resp = client.get("/secret")
        assert resp.status_code == 404
        assert resp.json() == {"detail": "Secret code not found"}
