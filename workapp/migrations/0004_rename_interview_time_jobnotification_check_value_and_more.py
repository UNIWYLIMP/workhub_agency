# Generated by Django 4.1.1 on 2023-05-13 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0003_jobnotification_interview_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobnotification',
            old_name='interview_time',
            new_name='check_value',
        ),
        migrations.AddField(
            model_name='application',
            name='interview_online',
            field=models.CharField(default='false', max_length=150),
        ),
        migrations.AlterField(
            model_name='application',
            name='interview_date',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='application',
            name='interview_time',
            field=models.CharField(default='', max_length=150),
        ),
    ]
