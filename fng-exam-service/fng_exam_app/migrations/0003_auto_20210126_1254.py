# Generated by Django 3.1.4 on 2021-01-26 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fng_exam_app', '0002_auto_20210123_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singleselectqa',
            name='correctAns',
            field=models.CharField(max_length=500),
        ),
    ]
