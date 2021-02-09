from django.db import models

 
# Create your models here.
class User(models.Model):
    userId = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    emailId = models.EmailField(max_length=100)
    createdBy = models.CharField(max_length=100)
    createdAt = models.DateTimeField()
    isDeleted = models.BooleanField(default=False)
    refreshToken = models.CharField(max_length=1000,null=True)
    def __str__(self):
        return self.userId
    class Meta:
        db_table ="user_details"

