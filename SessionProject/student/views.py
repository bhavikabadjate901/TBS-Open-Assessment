from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from student.utils import generate_access_token, generate_refresh_token,verify_access_token,verify_refresh_token
import json
from .models import User
import time,datetime
import requests
from .middleware import verify_token

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
            response = {'msg':' Added'}
        return JsonResponse(response,safe= False, status = 201)  # created
    except Exception as error:
        print("err", error)
        response = {'msg':'failure'}
    return JsonResponse(response,safe= False, status = 400) # bad request


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
                    status_code=200
                    response = {'msg':'Login Success','access_token': access_token}
                else:
                    response = {'msg':'Login failure'}
                    status_code=400
                return JsonResponse(response,safe= False, status = status_code)  # created
            except Exception as error:
                print(error)
    except Exception as error:
        print("err", error)
        response = {'Error':'Login'}
    return JsonResponse(response,safe= False, status = 400) # bad request

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


def setsession(request):
    request.session.set_expiry(60)
    request.session['token'] = generate_access_token()
    data = {'sussess': request.session['token'] } 
    return JsonResponse(data,safe=False)

def getsession(request):
    try:
        token = request.session.get('token')
        print(request.session.get_expiry_age())
        data = {'sussess in getting session': token}
        return JsonResponse(data,safe=False)
    except:
        data = {'Session is not available'}
        return JsonResponse(data, safe=False)       

def delsession(request):
    if 'token' in request.session:
        del request.session['token']
        return HttpResponse(request)
