import os
import boto3
import logging

from botocore.exceptions import ClientError

from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


"""
This code is based on an example found here:
    https://docs.aws.amazon.com/ses/latest/dg/send-an-email-using-sdk-programmatically.html

Another example:
    https://docs.aws.amazon.com/ses/latest/dg/send-email-raw.html#:%7E:text=Java-,Python,-The%20following%20code
"""


logger = logging.getLogger(__name__)
AWS_REGION = "us-east-1"
CHARSET = "UTF-8"


def send(attachments_dir: str = None):
    """
    By default, all the attachments should be uploaded to $LAMBDA_TASK_ROOT/attachments
    """
    if attachments_dir is None:
        attachments_dir = os.path.join(os.environ.get('LAMBDA_TASK_ROOT'), "attachments")

    #
    client = boto3.client('ses', region_name=AWS_REGION)

    #
    # This address must be verified with Amazon SES.
    sender = f"Alexey Lukyanov <{os.environ.get('SES_EMAIL')}>"

    # This address must be verified until the account is in the sandbox
    recipient = os.environ.get('SES_VERIFIED_RECIPIENT')

    logger.info(f"Environment:")
    logger.info(f"sender={sender}")
    logger.info(f"recipient={recipient}")

    # This file must be moved to the root of the lambda archive.
    # So, I have created a separate dir 'images' at the root of the
    # repo and add the images to lambda code.
    attachment1_path = os.path.join(attachments_dir, "attachment1.jpg")

    # The subject line for the email.
    subject = "Amazon SES Test (SDK for Python)"

    # The email body for recipients with non-HTML email clients.
    body_text = (
        "Amazon SES Test (Python)\r\n"
        "This email was sent with Amazon SES using the "
        "AWS SDK for Python (Boto)."
    )

    # The HTML body of the email.
    body_html = """<html>
    <head></head>
    <body>
      <h1>Amazon SES Test (SDK for Python)</h1>
      <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>AWS SDK for Python (Boto)</a>.
        <img src="cid:attachment1">
        <img src="cid:attachment2">
      </p>
    </body>
    </html>
    """

    # This is the main message
    msg = MIMEMultipart('mixed')

    # Add subject, from and to lines.
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Create a multipart/alternative child container.
    # This is an alternative container that is going to be displayed if client doesn't support
    # HTML embeddings.
    msg_body = MIMEMultipart('alternative')

    # Encode the text and HTML content and set the character encoding.
    # This step is necessary if you're sending a message with characters
    # outside the ASCII range.
    text_part = MIMEText(body_text, 'plain', CHARSET)
    html_part = MIMEText(body_html, 'html', CHARSET)

    # Add the text and HTML parts to the child container.
    msg_body.attach(text_part)
    msg_body.attach(html_part)

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    #
    # Attachments:
    #   There are two types of attachments - embedded and in mail.
    #
    # Define the attachment part and encode it using MIMEApplication.
    with open(attachment1_path, 'rb') as fid:
        att = MIMEApplication(fid.read())

        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        att.add_header(
            'Content-Disposition',
            'attachment1',
            filename=os.path.basename(attachment1_path))

    with open(attachment1_path, 'rb') as fid:
        msg_image = MIMEImage(fid.read())
        msg_image.add_header('Content-ID', '<attachment2>')
        msg.attach(msg_image)

    # Add the attachment to the parent container.
    msg.attach(att)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        # response = client.send_email(
        #     Destination={
        #         'ToAddresses': [
        #             recipient,
        #         ],
        #     },
        #     Message={
        #         'Body': {
        #             # This is an HTML version of the message
        #             'Html': {
        #                 'Charset': CHARSET,
        #                 'Data': body_html,
        #             },
        #             # This is a raw text version of the message for high-latency network
        #             'Text': {
        #                 'Charset': CHARSET,
        #                 'Data': body_text,
        #             },
        #         },
        #         'Subject': {
        #             'Charset': CHARSET,
        #             'Data': subject,
        #         },
        #     },
        #     Source=sender,
        #     # If you are not using a configuration set, comment or delete the
        #     # following line
        #     # ConfigurationSetName=CONFIGURATION_SET,
        # )
        response = client.send_raw_email(
            Source=sender,
            Destinations=[
                recipient
            ],
            RawMessage={
                'Data': msg.as_string(),
            },
            # ConfigurationSetName=CONFIGURATION_SET
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        logger.info(e.response['Error']['Message'])
    else:
        logger.info("Email sent! Message ID:"),
        logger.info(response['MessageId'])
