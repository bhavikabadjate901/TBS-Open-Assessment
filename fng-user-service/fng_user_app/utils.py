import datetime
import jwt
from django.conf import settings
from rest_framework import exceptions

# Author : Bhavika Badjate
# Date : 28-12-2020
# Function Desc : This function is used for genrate access token
# parameter : emailId
# return : access token
def generate_access_token(data):
    access_token_payload = {
        'emailId': data,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60) ,
        'iat': datetime.datetime.utcnow(),
    }
    # print(userId)
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    decoded_jwt = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
    return access_token

# Author : Bhavika Badjate
# Date : 28-12-2020
# Function Desc : This function is used for genrate refresh token
# parameter : emailId
# return : refresh token
def generate_refresh_token(data):
    refresh_token_payload = {
        'emailId': data,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256').decode('utf-8')
    return refresh_token

# Author : Bhavika Badjate
# Date : 29-12-2020
# Function Desc : This function is used to verify access token
# parameter : token
# return : emailId, status_code if valid else return error msg
def verify_access_token(token):
    data = {}
    if token:
        try:
            decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])  # JWT verify
            # if 
            data['isExpired'] = False
            data['emailId'] = decoded_jwt['emailId']
            data['msg'] = "Valid Signature"
            data['status_code'] = 200
        except jwt.ExpiredSignatureError:
            data['isExpired'] = True
            data['msg'] = "Expired Signature" 
            data['status_code'] = 401       # expired - 401
            decoded_jwt = jwt.decode(token, settings.SECRET_KEY ,options={'verify_exp': False}) 
            data['emailId'] = decoded_jwt['emailId']
        except jwt.InvalidSignatureError:
            data['msg'] = "Invalid Signature"
            data['status_code'] = 498       # invalid - 498
        except jwt.DecodeError:
            data['msg'] = "Token failed in validation"
            data['status_code'] = 403
        except jwt.InvalidTokenError:
            data[msg] = "Invalid token"
            data['status_code'] = 498       # invalid - 498
        return data

# Author : Bhavika Badjate
# Date : 29-12-2020
# Function Desc : This function is used to verify refresh token
# parameter : token
# return : emailId, status_code if valid else return error msg
def verify_refresh_token(token):
    data = {}
    if token:
        try:
            decoded_jwt1 = jwt.decode(token, settings.REFRESH_TOKEN_SECRET, algorithms=["HS256"])  # JWT verify
            # if 
            data['isExpired'] = False
            data['emailId'] = decoded_jwt1['emailId']
            data['msg'] = "Valid Signature"
            data['status_code'] = 200
        except jwt.ExpiredSignatureError:
            data['isExpired'] = True
            data['msg'] = "Expired Signature" 
            data['status_code'] = 401 # expired - 401
            decoded_jwt = jwt.decode(token, settings.REFRESH_TOKEN_SECRET ,options={'verify_exp': False}) 
            data['emailId'] = decoded_jwt['emailId']
        except jwt.InvalidSignatureError:
            data['msg'] = "Invalid Signature"
            data['status_code'] = 498       # invalid - 498
        except jwt.DecodeError:
            data[msg] = "Token failed in validation"
            data['status_code'] = 403
        except jwt.InvalidTokenError:
            data[msg] = "Invalid token"
            data['status_code'] = 498       # invalid - 498
        except jwt.InvalidIssuedAtError:
            data[msg] = "Invalid Issued"
            data['status_code'] = 498 
        return data

