from django.contrib import admin

# Register your models here.

from .models import EmailNotifications
admin.site.register(EmailNotifications)