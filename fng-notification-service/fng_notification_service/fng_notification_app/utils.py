from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage  
from string import Template

# function takes subject, template, and data needed for formatting 
# after formatting template trigger the mail and send the response
def template_to_msg(subNtemplate,dynamic_data_for_template): 
    subject = subNtemplate['subject']
    template = subNtemplate['template']
    emailId = dynamic_data_for_template['emailId']
    password = dynamic_data_for_template['password'] 
    formated_msg = template.format(username=emailId, password = password) # function return formated msg
    s = send_mail(subject,formated_msg, settings.EMAIL_HOST_USER,[emailId],fail_silently=False) # trigger mail
    if s >= 1:
        response = {'Success':'Successfully Send'}
    else: 
        response = {'Fail':'msg not send'}
    return response

