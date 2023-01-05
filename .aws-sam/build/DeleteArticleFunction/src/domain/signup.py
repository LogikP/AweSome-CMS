import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
USER_POOL_ID = 'eu-west-1_IkpDmJiBt'
CLIENT_ID = '15ud8n333ju19f96n7sopil76m'
CLIENT_SECRET = '1k8fcjjkr8c01iujl22hjcostpurapml01fik6avct1d54kfua9b'


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def lambda_handler(body):
    # body = json.loads(body)
    
    # for field in [body["username"], body["email"], body["password"], body["name"]]:
    #     if not body.get(field):
    #         return {"statusCode": 400, "isBase64Encoded": False, 'body': {"message": f"{field} is not present"}}
    username = body['username']
    email = body["email"]
    password = body['password']
    client = boto3.client('cognito-idp')
    try:
        resp = client.sign_up(
        ClientId=CLIENT_ID,
        SecretHash=get_secret_hash(username),
        Username=username,
        Password=password, 
        UserAttributes=[
        {
            'Name': "email",
            'Value': email
        }
        ],
        ValidationData=[
            {
                'Name': "email",
                'Value': email
            },
            {
                'Name': "custom:username",
                'Value': username
            }
        ])
    
    
    except client.exceptions.UsernameExistsException as e:
        return {
            "statusCode": 401,
            "headers": {},
            "body": json.dumps({
                "message": "Username Already Exists"
            })
        }
    except client.exceptions.InvalidPasswordException as e:
        return {
            "statusCode": 401,
            "headers": {},
            "body": json.dumps({
                "message": "Password should have Caps,\
                          Special chars, Numbers"
            })
        }
        
    except client.exceptions.UserLambdaValidationException as e:
        return {
            "statusCode": 401,
            "headers": {},
            "body": json.dumps({
                "message": "Email Already Exists"
            })
        }
    except Exception as e:
        return {
            "statusCode": 401,
            "headers": {},
            "body": json.dumps({
                "message": str(e)
            })
        }
    
    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({
                "message": "Please Confirm You're email address"
        })
    }