# Generated by Django 4.1.1 on 2023-05-22 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workapp', '0007_alter_jobpost_job_pay'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ManyToManyField(default=[0], related_name='chat_user_list', to='workapp.profile')),
            ],
            options={
                'db_table': 'Chat',
            },
        ),
        migrations.CreateModel(
            name='Chatmessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(default=None, max_length=3000)),
                ('time_sent', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workapp.chat')),
                ('sender', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='chat_sender', to='workapp.profile')),
            ],
            options={
                'db_table': 'Chat Message',
            },
        ),
    ]
