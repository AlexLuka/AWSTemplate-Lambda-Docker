#!/bin/bash

# The following environment variables are required
#   AWS_REGION
#   AWS_ACCOUNT_ID
#   SES_EMAIL
#   SES_VERIFIED_RECIPIENT

#
#
# First create IAM role and required polices
LAMBDA_FUNCTON_NAME=SendEmail-DockerImageTemplate
ROLE_NAME=AWSLambda-TemplateExample-Docker

#
# Create a lambda function with corresponding name and role
# The environment variables are used only in the code. If your code has different
# functionality you may create alternative environment variables.
aws lambda create-function                \
  --function-name ${LAMBDA_FUNCTON_NAME}  \
  --package-type Image                    \
  --code ImageUri=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/templates/lambda-docker:latest    \
  --no-paginate                           \
  --region ${AWS_REGION}                  \
  --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/${ROLE_NAME}     \
  --timeout 60                            \
  --environment "Variables={SES_EMAIL=${SES_EMAIL},SES_VERIFIED_RECIPIENT=${SES_VERIFIED_RECIPIENT}}"
