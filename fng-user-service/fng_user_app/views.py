from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
import json
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
import time,datetime
import requests
from .models import User
from rest_framework import status
import django
from .utils import generate_access_token, generate_refresh_token,verify_access_token,verify_refresh_token
from .middleware import verify_token


# Author : Bhavika Badjate
# Date : 13-12-2020
# Function Desc : This function is used for user registration
# Input : EmailId, Password
# Output : sucessfull/errror msg
@csrf_exempt
def user_registration(request):
    try:
        payload =json.loads(request.body)
        if 'emailId' in payload and payload['emailId'] and 'password' in payload and payload['password']:
            user = User.objects.filter(emailId= payload['emailId'])
            if user:
                response = {'msg':'User already Exists'}
                return JsonResponse(response,safe= False, status = 200)  #OK
            new_user = User()
            new_user.userId = "UID" + str(time.time_ns())[:15]
            new_user.emailId = payload['emailId']
            new_user.password = payload['password']
            new_user.createdBy = "MOD1234"
            new_user.createdAt = datetime.datetime.now()
            new_user.save()
            templateId = 1
            response = {'msg' :'Succesfully Added'}
            dynamic_data_for_template = {'emailId' : new_user.emailId, 'password' : new_user.password, 'templateId':templateId}  #templateId
            r = requests.post('http://127.0.0.1:3000/get_msg/', data = json.dumps(dynamic_data_for_template)) 
        return JsonResponse(response,safe= False, status = 201)  # created
    except Exception as error:
        print("err", error)
        response = {'msg':'failure'}
    return JsonResponse(response,safe= False, status = 400) # bad request

# Author : Bhavika Badjate
# Date : 15-12-2020
# Function Desc : This function is used to login
# Input : EmailId, Password
# Output : if EmailId and Password is valid then - login successful else error msg
@csrf_exempt
def user_login(request):
    try:
        payload =json.loads(request.body)
        if 'emailId' in payload and payload['emailId'] and 'password' in payload and payload['password']:
            try:
                user = User.objects.get(emailId= payload['emailId'], password=payload['password'])
                if user:
                    access_token = generate_access_token(payload['emailId'])
                    user.refreshToken = generate_refresh_token(payload['emailId'])
                    user.save()
                    response = {'msg':'Login Success','access_token': access_token}
                    status_code=200
                else:
                    response = {'msg':'Login failure'}
                    status_code=400
                return JsonResponse(response,safe= False, status = status_code)  # created
            except Exception as error:
                print(error)
                print("err", error)
                response = {'Error':'Login'}
                status_code = 400
    except Exception as error:
        print("err", error)
        response = {'Error':'Login'}
        status_code = 400
    return JsonResponse(response,safe= False, status = status_code) # bad request

# Author : Bhavika Badjate
# Date : 15-12-2020
# Function Desc : This function is used to login
# Input : EmailId, Password
# Output : if EmailId and Password is valid then - login successful else error msg
@csrf_exempt
def view_users(request):
    try:
        data = list(User.objects.values())
        # print(data)
        return JsonResponse(data, safe=False,status=201) 
    except Exception as error:
        return JsonResponse(safe=False, status = 400)

# Author : Bhavika Badjate
# Date : 20-12-2020
# Function Desc : This function is used to upload users data
# Input : bulk data of users
# Output : fail count, success count, fail data
@csrf_exempt
def bulk_user_upload(request):
    try:
        payload = json.loads(request.body)
        if 'data' in payload and len(payload['data']) > 0:
            success_count = 0
            fail_count = 0
            fail_data = []
            for record in payload['data']:
                if 'emailId' in record and record['emailId'] != "" and 'password' in record and record['password'] != "":
                    user = User.objects.filter(emailId = record['emailId'])
                    if not user:
                        new_user = User()
                        new_user.userId = "UID" + str(time.time_ns())[:15]
                        new_user.emailId = record['emailId']
                        new_user.password = record['password']
                        new_user.createdBy = "MOD1234"
                        new_user.createdAt = datetime.datetime.now()
                        new_user.save()
                        success_count += 1
                    else:
                        data = {}
                        fail_count += 1
                        data['emailId'] = record['emailId']
                        data['reason'] = "User Already Exists"
                        fail_data.append(data)
                        continue
                else:
                    data = {}
                    fail_count += 1
                    if(record['emailId'] == ""):
                        data['emailId'] = "NULL"
                        data['reason'] = "EmailId Missing"
                    else:
                        data['emailId'] = record['emailId']
                        data['reason'] = "Password Missing"
                    fail_data.append(data)
                    continue
            response = {
                'success_count': success_count,
                'fail_count':fail_count,
                'fail_data':fail_data,
                'msg': 'Data uploaded Successfully'
            }
            status_code = 201
        else:
            response = {
                'msg': 'Failure'
            }
            status_code = 400
    except Exception as err:
        print(err)
        response = {
                'msg': 'failure',
                'error':err
        }
        status_code = 400
    return JsonResponse(response,safe=False, status = status_code)


# Author : Bhavika Badjate
# Date : 15-12-2020
# Function Desc : This function is used to get all the data of users
@csrf_exempt
@verify_token
def user_logout(request):
    try:
        token =json.loads(request.body)
        data = verify_access_token(token['access_token'])
        user = User.objects.get(emailId= data['emailId'])
        if user.refreshToken != "":
            user.refreshToken = ""
            user.save()
            response = {'msg':'Logout Successfull'}
            status_code=200
        else:
            response = {'msg':'Aready Logout'}
            status_code=200
    except Exception as error:
        print(error)
        response = {'msg':'Logout failure'}
        status_code=400
    return JsonResponse(response,safe= False, status = status_code)
