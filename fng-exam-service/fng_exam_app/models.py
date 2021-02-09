from django.db import models
# Create your models here.
# from django_mysql.models import JSONField
from django_base64field.fields import Base64Field
from django.contrib.postgres.fields import ArrayField

class WaitageOfQuestions(models.Model):
    subjectId = models.CharField(max_length=100,primary_key=True)
    totalNumberQuestions = models.IntegerField()
    unknownNoQuestions = models.IntegerField(default=0)
    easyNoQuestions = models.IntegerField(default=0)
    mediumNoQuestions = models.IntegerField(default=0)
    hardNoQuestions = models.IntegerField(default=0)
    class Meta:
        db_table = "WaitageOfQuestions"

class SingleSelectQA(models.Model):
    question = models.CharField(max_length= 500)
    difficultyLevel = models.IntegerField(default= 0) # 0 - mix, 1 - easy, 2 - medium, 3 - hard
    optionA = models.CharField(max_length=200)
    optionB = models.CharField(max_length=200)
    optionC = models.CharField(max_length=200)
    optionD = models.CharField(max_length=200)
    correctAns = models.CharField(max_length=500)
    questionId = models.CharField(max_length=100)
    subjectId = models.CharField(max_length=100)
    class Meta:
        db_table = "SingleSelectQA"

class MultiSelectQA(models.Model):
    question = models.CharField(max_length= 500)
    difficultyLevel = models.IntegerField(default= 0) # 0 - unknown 1 - easy, 2 - medium, 3 - hard
    optionsA = models.CharField(max_length=200)
    optionsB = models.CharField(max_length=200)
    optionsC = models.CharField(max_length=200)
    optionsD = models.CharField(max_length=200)
    correctAns = ArrayField(models.CharField(max_length=200), blank=True)
    questionId = models.CharField(max_length=100)
    subjectId = models.CharField(max_length=100)
    # questionType = models.BooleanField(default=False) # True - Image , False - text
    # questionImg = Base64Field(max_length=900000, blank=True, null=True)   # for questionType Image
    class Meta:
        db_table = "MultiSelectQA"