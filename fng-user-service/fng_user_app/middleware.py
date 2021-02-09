from .utils import generate_access_token,generate_refresh_token, verify_access_token,verify_refresh_token
import json
from .models import User
from django.http import HttpResponse, JsonResponse

# Author : Bhavika Badjate
# Date : 30-12-2020
# Function Desc : This function is used to verify token
# Input : token
# Output : after verifying access token if status code is 200 which return request
#          if stataus code is 401 then return response of new access token else return error msg
def verify_token(get_response):
    def middleware(request):
        try:
            access_token = json.loads(request.body)
            data = verify_access_token(access_token['access_token'])
            if data['status_code'] == 200 or data['status_code'] == 401:
                if data['status_code'] == 200:
                    response = get_response(request)
                    return response
                else:
                    user = User.objects.get(emailId = data['emailId'])
                    data1 = verify_refresh_token(user.refreshToken)
                    new_access_token = generate_access_token(data['emailId'])
                    if data1['status_code'] == 200:
                        return JsonResponse({'New_Access_Token': new_access_token},safe=False,status = data1['status_code'])
                    elif data1['status_code'] == 401:
                        return JsonResponse({'New_Access_Token': new_access_token},safe=False,status = data1['status_code'])
                    else:
                        return JsonResponse(data1, safe=False,status = data1['status_code'])   
            else:
                return JsonResponse(data, safe=False,status = data['status_code'])
        except Exception as error:
            print("err", error)
            response = {'msg':'failure'}
            return JsonResponse(response,safe= False, status = 400)
    return middleware

