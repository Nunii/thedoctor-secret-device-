#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Starting verification script..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running${NC}"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose > /dev/null 2>&1; then
    echo -e "${RED}Error: docker-compose is not installed${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    exit 1
fi

# Start the service
echo "Starting service..."
docker-compose up -d

# Wait for the service to start
echo "Waiting for service to start..."
sleep 5

# Test health endpoint
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://127.0.0.1:5000/health)

# Validate health response format
if [[ $HEALTH_RESPONSE == *"status"* && $HEALTH_RESPONSE == *"container"* && $HEALTH_RESPONSE == *"project"* ]]; then
    # Extract values using grep and sed
    STATUS=$(echo $HEALTH_RESPONSE | grep -o '"status": *"[^"]*"' | sed 's/"status": *"\([^"]*\)"/\1/')
    CONTAINER=$(echo $HEALTH_RESPONSE | grep -o '"container": *"[^"]*"' | sed 's/"container": *"\([^"]*\)"/\1/')
    PROJECT=$(echo $HEALTH_RESPONSE | grep -o '"project": *"[^"]*"' | sed 's/"project": *"\([^"]*\)"/\1/')

    # Validate each field
    if [[ "$STATUS" == "healthy" && \
          "$CONTAINER" == *"hub.docker.com"* && \
          "$PROJECT" == *"github.com"* ]]; then
        echo -e "${GREEN}Health endpoint is working${NC}"
        echo "Health response: $HEALTH_RESPONSE"
    else
        echo -e "${RED}Health endpoint response format is incorrect${NC}"
        echo "Expected: { status: healthy, container: <LINK_TO_HUB>, project: github.com/omerxx/ecscale }"
        echo "Got: $HEALTH_RESPONSE"
        docker-compose down
        exit 1
    fi
else
    echo -e "${RED}Health endpoint is not working${NC}"
    echo "Response: $HEALTH_RESPONSE"
    docker-compose down
    exit 1
fi

# Test secret endpoint
echo "Testing secret endpoint..."
SECRET_RESPONSE=$(curl -s http://127.0.0.1:5000/secret)
if [[ $SECRET_RESPONSE == *"secret_code"* ]]; then
    echo -e "${GREEN}Secret endpoint is working${NC}"
    echo "Secret response: $SECRET_RESPONSE"
else
    echo -e "${RED}Secret endpoint is not working${NC}"
    echo "Response: $SECRET_RESPONSE"
    docker-compose down
    exit 1
fi

# Stop the service
echo "Stopping service..."
docker-compose down

echo -e "${GREEN}Verification completed successfully!${NC}"
exit 0

