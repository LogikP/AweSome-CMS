import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid
USER_POOL_ID = 'eu-west-1_IkpDmJiBt'
CLIENT_ID = '15ud8n333ju19f96n7sopil76m'
CLIENT_SECRET = '1k8fcjjkr8c01iujl22hjcostpurapml01fik6avct1d54kfua9b'

def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2
    
def confirm_signup_function(body):
    client = boto3.client('cognito-idp')
    try:
        username = body['username']
        password = body['password']
        code = body['code']
        response = client.confirm_sign_up(
        ClientId=CLIENT_ID,
        SecretHash=get_secret_hash(username),
        Username=username,
        ConfirmationCode=code,
        ForceAliasCreation=False,
       )
    except client.exceptions.UserNotFoundException:
        return {
            "statusCode": 401,
            "headers": {},
            "body": json.dumps({
                "message": "Username Dosent exists"
            })
        }
    except client.exceptions.CodeMismatchException:
        return {
            "statusCode": 401,
            "headers": {},
            "body": json.dumps({
                "message": "Invalid Verification code"
            })
        }
        
    except client.exceptions.NotAuthorizedException:
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({
                "message": "User Already Confirmed"
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {},
            "body": json.dumps({
                "message": str(e)
            })
        }
    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({
            "message": "User confirmed"
        })
    }