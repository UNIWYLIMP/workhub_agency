from django.contrib import admin
from .models import *

models = [JobPost, JobNotification, JobRole, JobCategory, JobRequirement, Application, Education, Experience, Skill,
          Profile, Chat, Chatmessage, ChatReported]

# Register your models here.
admin.site.register(models)
