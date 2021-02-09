from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from .models import EmailNotifications
from rest_framework import status
from .utils import template_to_msg
from anymail.signals import tracking
from django.dispatch import receiver
from pyfcm import FCMNotification
from django.core import serializers
# Create your views here.


@csrf_exempt
def save_msg(request):
    
    payload = json.loads(request.body)
    if 'templateId' in payload and payload['templateId'] and'subject' in payload and payload['subject'] and 'template' in payload and payload['template']:
        msg = EmailNotifications.objects.filter(subject = payload['subject'])
        new_msg = msg()
        new_msg.templateId = payload['templateId']
        new_msg.subject = payload['subject']
        new_msg.template = payload['template']
        new_user.save()
        response = {'msg':'Succesfully Added'}
    return JsonResponse(response,safe= False, status = 201)

@csrf_exempt
def get_template_send_mail(request):
    try:
        dynamic_email_data = json.loads(request.body)  #get dynamic_data to send mail like templateId,name,emailId and many more
        print(dynamic_email_data)
        subNtemplate = EmailNotifications.objects.filter(templateId = dynamic_email_data['templateId'])
        subNtemplate = serializers.serialize('json',subNtemplate)
        subNtemplate = json.loads(subNtemplate)
        subNtemplate = subNtemplate[0]['fields']
        response = template_to_msg(subNtemplate,dynamic_email_data)  # this line call the function which is written in utils.py and returns response
        return JsonResponse(response, safe=False,status=201) 
    except Exception as error:
        print(error)
        response = {'err': error}
        return JsonResponse(response,safe=False, status = 400)



