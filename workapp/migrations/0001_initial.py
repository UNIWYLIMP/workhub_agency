# Generated by Django 4.1.1 on 2023-05-12 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_status', models.CharField(default='pending', max_length=50)),
                ('interview_date', models.CharField(max_length=150)),
                ('interview_time', models.CharField(max_length=150)),
                ('interview_location_url', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'Application',
            },
        ),
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=150)),
                ('job_description', models.CharField(max_length=150)),
                ('job_type', models.CharField(default='On-Site', max_length=50)),
                ('job_pay', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'Job Post',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userEmail', models.EmailField(default='', max_length=250)),
                ('userName', models.CharField(default='', max_length=50)),
                ('userFullName', models.CharField(default='', max_length=50)),
                ('userTitle', models.CharField(default='', max_length=100)),
                ('userContact', models.CharField(default='+(000)000-000-000', max_length=50)),
                ('userBio', models.CharField(default='', max_length=500)),
                ('userType', models.CharField(default='employee', max_length=100)),
                ('userProfilePicture', models.ImageField(blank=True, null=True, upload_to='profile_picture/')),
                ('userResume', models.FileField(blank=True, null=True, upload_to='resume(cv)/')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_set', models.CharField(max_length=50)),
                ('proficiency', models.CharField(max_length=10)),
                ('userProfile', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workapp.profile')),
            ],
            options={
                'db_table': 'Skill Sets',
            },
        ),
        migrations.CreateModel(
            name='JobRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=500)),
                ('job', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workapp.jobpost')),
            ],
            options={
                'db_table': 'Job Role',
            },
        ),
        migrations.CreateModel(
            name='JobRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requirement', models.CharField(max_length=500)),
                ('job', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workapp.jobpost')),
            ],
            options={
                'db_table': 'Job Requirement',
            },
        ),
        migrations.AddField(
            model_name='jobpost',
            name='job_poster',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workapp.profile'),
        ),
        migrations.CreateModel(
            name='JobNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_sent', models.DateTimeField(auto_now_add=True)),
                ('job_application', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workapp.application')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workapp.profile')),
            ],
            options={
                'db_table': 'Job Notification',
            },
        ),
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=150)),
                ('job', models.ManyToManyField(default=[0], to='workapp.jobpost')),
            ],
            options={
                'db_table': 'Job Category',
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Experience_Title', models.CharField(max_length=50)),
                ('Experience_Employment_Type', models.CharField(max_length=50)),
                ('Experience_Organization_Name', models.CharField(max_length=50)),
                ('Experience_Location', models.CharField(max_length=50)),
                ('Experience_Start_Date', models.CharField(max_length=50)),
                ('Experience_Close_Date', models.CharField(max_length=50)),
                ('userProfile', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workapp.profile')),
            ],
            options={
                'db_table': 'Working Experience',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=50)),
                ('degree', models.CharField(max_length=50)),
                ('field', models.CharField(max_length=50)),
                ('startDate', models.CharField(max_length=25)),
                ('endDate', models.CharField(max_length=25)),
                ('description', models.CharField(max_length=5000)),
                ('userProfile', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workapp.profile')),
            ],
            options={
                'db_table': 'Education',
            },
        ),
        migrations.AddField(
            model_name='application',
            name='job',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workapp.jobpost'),
        ),
        migrations.AddField(
            model_name='application',
            name='job_applicant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workapp.profile'),
        ),
    ]
