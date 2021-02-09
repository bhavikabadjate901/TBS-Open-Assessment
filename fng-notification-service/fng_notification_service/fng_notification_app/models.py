from django.db import models

# Create your models here.

class EmailNotifications(models.Model):
    templateId = models.CharField(max_length=100,primary_key=True)
    subject = models.CharField(max_length=200)
    template = models.CharField(max_length=600)
    class Meta:
        db_table = "EmailNotifications"

