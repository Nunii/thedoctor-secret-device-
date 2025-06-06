# Secret Device Service - Setup and Usage Instructions

## Prerequisites
- Python 3.11 or higher
- Docker and Docker Compose
- Git

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/Nunii/secret-device-service.git
cd secret-device-service
```

2. Create a `.env` file in the root directory with the following variables:
```env
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
CODE_NAME=your_code_name
DOCKER_HUB_LINK=https://hub.docker.com/r/your_username/secret-device
GITHUB_PROJECT_LINK=https://github.com/your_username/secret-device-service
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run tests:
```bash
pytest --cov=app test/
```

5. Start the service using Docker Compose:
```bash
docker-compose up --build
```

The service will be available at:
- Health check: http://127.0.0.1:5000/health
- Secret endpoint: http://127.0.0.1:5000/secret

## Running Tests

1. Install test dependencies:
```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

2. Run tests with coverage:
```bash
pytest --cov=app test/
```

## Docker Usage

1. Build the Docker image:
```bash
docker build -t secret-device .
```

2. Run the container:
```bash
docker run -p 5000:5000 --env-file .env secret-device
```

## AWS Deployment

1. Install AWS CLI and configure credentials:
```bash
aws configure
```

2. Deploy using CloudFormation:
```bash
aws cloudformation create-stack \
  --stack-name secret-device \
  --template-body file://environment.template \
  --parameters \
    ParameterKey=VpcId,ParameterValue=your_vpc_id \
    ParameterKey=SubnetIds,ParameterValue=subnet1,subnet2 \
    ParameterKey=DatabasePassword,ParameterValue=your_db_password \
    ParameterKey=DockerImage,ParameterValue=your_docker_image \
    ParameterKey=DockerUsername,ParameterValue=your_docker_username \
    ParameterKey=DockerToken,ParameterValue=your_docker_token \
    ParameterKey=CodeName,ParameterValue=your_code_name
```

## Verification

Run the verification script:
```bash
./verification.sh
```

## API Endpoints

### Health Check
- **URL**: `/health`
- **Method**: GET
- **Response**: 
```json
{
  "status": "healthy",
  "container": "https://hub.docker.com/r/your_username/secret-device",
  "project": "https://github.com/your_username/secret-device-service"
}
```

### Secret
- **URL**: `/secret`
- **Method**: GET
- **Response**:
```json
{
  "secret_code": "your_code"
}
```

## Troubleshooting

If you encounter any issues:
1. Check the logs: `docker-compose logs`
2. Verify environment variables are set correctly
3. Ensure all dependencies are installed
4. Check the TROUBLE.md file for common issues and solutions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 