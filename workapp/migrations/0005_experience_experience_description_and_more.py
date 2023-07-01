# Generated by Django 4.1.1 on 2023-05-13 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0004_rename_interview_time_jobnotification_check_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='Experience_Description',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='experience',
            name='Experience_Close_Date',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='experience',
            name='Experience_Employment_Type',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='experience',
            name='Experience_Location',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='experience',
            name='Experience_Organization_Name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='experience',
            name='Experience_Start_Date',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='experience',
            name='Experience_Title',
            field=models.CharField(default='', max_length=50),
        ),
    ]