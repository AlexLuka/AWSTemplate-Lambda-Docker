#!/bin/bash

# Run this script with command:
#       dotenv -e ../../../.env -- ./create-iam-role.sh
# because .env file contains AWS_REGION variable

# Policy that allows to pul images from ECR: AmazonEC2ContainerRegistryPullOnly

ROLE_NAME=AWSLambda-TemplateExample-Docker
#POLICY_NAME=AWSLambda-TemplateExample-Docker-ECRAccessPolicy

aws iam create-role \
  --role-name ${ROLE_NAME} \
  --assume-role-policy-document file://$(pwd)/iam-role.json \
  --region ${AWS_REGION} \
  --no-paginate


# ARN will be "arn:aws:iam::***:policy/AWSLambda-EmailSubmissionTemplate-SESAccessPolicy"
#aws iam create-policy \
#  --policy-name ${POLICY_NAME} \
#  --policy-document file://$(pwd)/ses-policy.json \
#  --description "Policy that should allow Lambda to send emails using SES" \
#  --region ${AWS_REGION} \
#  --no-paginate
#
#
#aws iam attach-role-policy \
#  --role-name ${ROLE_NAME} \
#  --policy-arn arn:aws:iam::${AWS_ACCOUNT_ID}:policy/${POLICY_NAME} \
#  --region ${AWS_REGION} \
#  --no-paginate
