import os
import boto3
from flask import flash, Flask, render_template, Blueprint
from dotenv import load_dotenv

# Loading Environment Variables
load_dotenv()

# Loading AWS Credentials

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEy')
# Creating EC2 Boto3 Client

ec2 = boto3.client(

    'ec2',
    aws_access_key_id = 'AWS_ACCESS_KEY_ID',
    aws_secret_access_key = 'AWS_SECRET_ACCESS_KEY'

)