from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import time,datetime 
import requests
from rest_framework import status
import django
from .models import MultiSelectQA,SingleSelectQA,WaitageOfQuestions
from fng_exam_service import commonFun
# from rest_framework import serializers
from django.core import serializers
import random
import bcrypt

@csrf_exempt
def single_select_bulk_QA_upload(request):
    try:
        payload = json.loads(request.body)
        if 'data' in payload and len(payload['data']) > 0:
            success_count = 0
            fail_count = 0
            fail_data = []
            for record in payload['data']:
                if 'question' in record and record['question'] != "":
                    # mcq_ans = SingleSelectQA.objects.filter(question = record['question'])
                    # if not mcq_ans:
                    new_ques_ans = SingleSelectQA()
                    new_ques_ans.questionId =  "QID" + str(time.time_ns())[:15]
                    new_ques_ans.subjectId = "SID" + str(time.time_ns())[:15]
                    new_ques_ans.question = record['question']
                    new_ques_ans.difficultyLevel = record['difficultyLevel']
                    new_ques_ans.optionA = record['optionA']
                    new_ques_ans.optionB = record['optionB']
                    new_ques_ans.optionC = record['optionC']
                    new_ques_ans.optionD = record['optionD']
                    CA = record['correctAns']
                    correctAns = commonFun.encode_msg(CA)
                    new_ques_ans.correctAns = correctAns    
                    new_ques_ans.save()
                    success_count += 1
                else:
                    data = {}
                    fail_count += 1
                    if(record['question'] == ""):
                        data['question'] = record['question']
                        data['reason'] = "Question is missing"
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
                'msg': 'Failure',
                'error':err
        }
        status_code = 400
    return JsonResponse(response,safe=False, status = status_code)


@csrf_exempt
def multiple_select_bulk_QA_upload(request):
    try:
        payload = json.loads(request.body)
        if 'data' in payload and len(payload['data']) > 0:
            success_count = 0
            fail_count = 0
            fail_data = []
            for record in payload['data']:
                if 'question' in record and record['question'] != "":
                    # mcq_ans = MultiSelectQA.objects.filter(question = record['question'])
                    # if not mcq_ans:
                    new_ques_ans = MultiSelectQA()
                    new_ques_ans.questionId =  "QID" + str(time.time_ns())[:15]
                    new_ques_ans.subjectId = "SID" + str(time.time_ns())[:15]
                    new_ques_ans.question = record['question']
                    new_ques_ans.difficultyLevel = record['difficultyLevel']
                    new_ques_ans.optionA = record['optionA']
                    new_ques_ans.optionB = record['optionB']
                    new_ques_ans.optionC = record['optionC']
                    new_ques_ans.optionD = record['optionD']
                    CA = record['correctAns']
                    correctAns = commonFun.encode_msg(CA)
                    new_ques_ans.correctAns = correctAns
                    # new_ques_ans.questionImg
                    new_ques_ans.save()
                    success_count += 1
                else:
                    data = {}
                    fail_count += 1
                    if(record['question'] == ""):
                        data['question'] = record['question']
                        data['reason'] = "Question is missing"
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
                'msg': 'Failure',
                'error':err
        }
        status_code = 400
    return JsonResponse(response,safe=False, status = status_code)

# Author:Bhavika Badjate
# Date: 20-12-2020
# Function Desc: This functtion is used to generate exam
# Input: subjectId,number of questions - easy, medium, hard
# Output: Array of Questions
@csrf_exempt
def generate_exam(request):
    try:
        totalNumberQuestions = 5
        unknownNoQuestions = 0
        easyNoQuestions = 5
        mediumNoQuestions = 0
        hardNoQuestions = 0

        questionIdList = SingleSelectQA.objects.values_list('questionId', 'difficultyLevel')
        QList = []
        if unknownNoQuestions !=0:
            QIDsUnknown = questionIdList.filter(difficultyLevel = 0).values_list('questionId', flat= True)
            totalQuestions = len(list(QIDsUnknown))                                                        
            questionSet = commonFun.RandomQuestions(list(QIDsUnknown), totalQuestions, unknownNoQuestions)
            QList = QList + questionSet

        if easyNoQuestions != 0:
            QIDsEasy = questionIdList.filter(difficultyLevel = 1).values_list('questionId', flat= True)
            totalQuestions = len(list(QIDsEasy))
            questionSet = commonFun.RandomQuestions( list(QIDsEasy), totalQuestions,easyNoQuestions)
            QList = QList + questionSet

        if mediumNoQuestions != 0:
            QIDsMedium = questionIdList.filter(difficultyLevel = 2).values_list('questionId', flat= True)
            totalQuestions = len(list(QIDsMedium))
            questionSet = commonFun.RandomQuestions( list(QIDsMedium), totalQuestions, mediumNoQuestions)
            QList = QList + questionSet
    
        if hardNoQuestions != 0:
            QIDsHard = questionIdList.filter(difficultyLevel = 3).values_list('questionId', flat= True)
            totalQuestions = len(list(QIDsHard))
            questionSet = commonFun.RandomQuestions( list(QIDsHard), totalQuestions, hardNoQuestions)
            QList = QList + questionSet
        
        QNA = SingleSelectQA.objects.filter(questionId__in = QList)

        QNA = serializers.serialize('json',QNA)
        QNA = json.loads(QNA)

        qna = []
        for i in QNA:
            data = {}
            data['questionId'] = i['fields']['questionId']
            data['question'] = i['fields']['question']
            data['optionA'] = i['fields']['optionA']
            data['optionB'] = i['fields']['optionB']
            data['optionC'] = i['fields']['optionC']
            data['optionD'] = i['fields']['optionD']
            print(data)
            qna.append(data)

        return JsonResponse(qna, safe=False,status=200) 
    except Exception as err:
        print(err)
        return JsonResponse(safe=False, status = 400)

@csrf_exempt
def generate_scorecard(request):
    payload = json.loads(request.body)
    if 'data' in payload and len(payload['data']) > 0:
        marks = 0
        for record in payload['data']:
            question = MultiSelectQA.objects.filter(questionId = record['questionId'])
            QNA = serializers.serialize('json',question)
            QNA = json.loads(QNA)
            for i in QNA:
                if type(record['selectedAns']) == str:
                    if i['fields']['correctAns'] == commonFun.encode_msg(record['selectedAns']):
                        marks += 1
                    else:
                        pass
                else:
                    s1 = i['fields']['correctAns']
                    res = s1.strip('][').split(', ')
                    if len(res) == len(commonFun.encode_msg(record['selectedAns'])):
                        pass
                    else:
                        pass
        response = {
                'marks': marks
        }
        return JsonResponse(response, safe=False,status=200) 
    else:
        response = {
                'msg': 'Failure',
                'error':err
        }
        status_code = 400
    return JsonResponse(response, safe=False,status=status_code)