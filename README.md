#

# Instructions to create a Docker image can be found here https://docs.aws.amazon.com/lambda/latest/dg/images-create.html


# Build image

Build image with the command

```shell
docker build -t aws-lambda-test --platform linux/amd64 . &> logs/build-$(date +%s).log
```

Then run it with 
```shell
docker run --platform linux/amd64 -p 9000:8080 aws-lambda-test:latest
```

This will start an attached process in a terminal session. In a separate session, execute a command
```shell
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```
If everything works, then you will see log messages in a main session.
More information can be found [here](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions).


# Push image to ECR

For automatic deployment, we are going to create a GitHubActions script that will build a docker 
image and push it to ECR. For GHA to work properly, you need to create AssumedRole that will
be used for interaction between GitHub and AWS. Then, you need to add the following variables
as secrets to the repo:
![](images/img1.png)

# Create IAM role and lambda function

# Update function on every push to main

As per [documentation](https://docs.aws.amazon.com/cli/latest/reference/lambda/update-function-code.html):
```text
For a function defined as a container image, Lambda resolves the image tag to an image digest. 
In Amazon ECR, if you update the image tag to a new image, Lambda does not automatically update 
the function.
```

This means that if we simply push image to ECR with tag _latest_, the function will not catch 
those changes and continue to use the old code. In order to update the function definition we
must add the following step to the GHA workflow:

```shell
aws lambda update-function-code \
    --function-name LambdaFunctionName \
    --image-uri ***.dkr.ecr.us-east-1.amazonaws.com/lambda-function-image-repo \
    --publish
```

There is a chance that when you run a workflow, you will get an error that the 
role, that is used by GitHub to update AWS resources, doesn't have permissions to update the code
on Lambda service.
To fix that, you need to add the following policy to the IAM role:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "lambda:UpdateFunctionCode",
            "Resource": "arn:aws:lambda:us-east-1:***:function:LambdaFunctionName"
        }
    ]
}
```

where *** indicate the account number ID. Alternatively, you can set "Resource" to a wildcard, but that
 violates the principle of the least privilege.
Therefore, it is recommended to indicate the resource explicitly.


# Send email resource

TODO
I did these steps a while ago and already have everything in place.
Need to refresh my memory about the steps that I did.
To send email you need to create a specific resource - destination of your email.


# Send email policy

In addition to resource, you would need to allow lambda function to access SES, and send 
emails to indicated resources. So, for that you need to add the following policy to your 
lambda role:
```json
{
    "Effect": "Allow",
    "Action": [
        "ses:SendEmail",
        "ses:SendRawEmail"
    ],
    "Resource": [
      "arn:aws:ses:us-east-1:***:identity/destination.email@domain.com",
      "arn:aws:ses:us-east-1:***:identity/your.domain.identity",
      "arn:aws:ses:us-east-1:***:configuration-set/domain-identity-configuration-set"
    ]
}
```

These are required for Lambda to send email from your _domain.identity_ to _destination.email_ .


# Frequent brakes

## urllib3

In the local environment I had a library version 2.2.3 while in Docker it was set to 1.26.19 .
I guess it was installed by default.
Anyway, that cause some problems during runtime.