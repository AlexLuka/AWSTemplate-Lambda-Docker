#!/bin/bash

# Run this script with command:
#       dotenv -e ../../../.env -- ./create-iam-role.sh
# because .env file contains AWS_REGION variable

ROLE_NAME=AWSLambda-TemplateExample-Docker

aws iam create-role \
  --role-name ${ROLE_NAME} \
  --assume-role-policy-document file://$(pwd)/iam-role.json \
  --region ${AWS_REGION} \
  --no-paginate
