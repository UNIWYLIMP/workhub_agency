from django.db import models


class Profile(models.Model):
    userEmail = models.EmailField(max_length=250, default="")
    userName = models.CharField(max_length=50, default="")
    userFullName = models.CharField(max_length=50, default="")
    userTitle = models.CharField(max_length=100, default="")
    userContact = models.CharField(max_length=50, default="+(000)000-000-000")
    userBio = models.CharField(max_length=500, default="")
    userType = models.CharField(max_length=100, default="employee")
    userDOB = models.CharField(max_length=100, default="-- -- --")
    userLocation = models.CharField(max_length=100, default="-- -- --")
    userGender = models.CharField(max_length=100, default="Male")
    userProfilePicture = models.ImageField(upload_to='profile_picture/', null=True, blank=True)
    userResume = models.FileField(upload_to='resume(cv)/', null=True, blank=True)
    userPassword = models.CharField(max_length=500, default="no_active_password")
    admin_conversation = models.CharField(max_length=500, default="none")


class Education(models.Model):
    school = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)
    field = models.CharField(max_length=50)
    startDate = models.CharField(max_length=25)
    endDate = models.CharField(max_length=25)
    description = models.CharField(max_length=5000)
    userProfile = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'Education'


class Skill(models.Model):
    skill_set = models.CharField(max_length=50)
    proficiency = models.CharField(max_length=10)
    userProfile = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'Skill Sets'


class Experience(models.Model):
    Experience_Title = models.CharField(max_length=50, default="")
    Experience_Employment_Type = models.CharField(max_length=50, default="")
    Experience_Organization_Name = models.CharField(max_length=50, default="")
    Experience_Description = models.CharField(max_length=500, default="")
    Experience_Location = models.CharField(max_length=50, default="")
    Experience_Start_Date = models.CharField(max_length=50, default="")
    Experience_Close_Date = models.CharField(max_length=50, default="")
    userProfile = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'Working Experience'


class JobPost(models.Model):
    job_title = models.CharField(max_length=150)
    job_description = models.CharField(max_length=150)
    job_type = models.CharField(max_length=50, default="On-Site")
    job_poster = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1)
    job_pay = models.CharField(max_length=200, default="")
    job_location = models.CharField(max_length=100, default="United States")
    job_external = models.CharField(max_length=50, default="none")
    job_external_link = models.CharField(max_length=5000, default="___")

    class Meta:
        db_table = 'Job Post'


class JobCategory(models.Model):
    category_name = models.CharField(max_length=150)
    job = models.ManyToManyField('JobPost', default=[0])

    class Meta:
        db_table = 'Job Category'


class JobRequirement(models.Model):
    requirement = models.CharField(max_length=500)
    job = models.ForeignKey('JobPost', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'Job Requirement'


class JobRole(models.Model):
    role = models.CharField(max_length=500)
    job = models.ForeignKey('JobPost', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'Job Role'


class Application(models.Model):
    job = models.ForeignKey('JobPost', on_delete=models.CASCADE, default=1)
    job_applicant = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1)
    application_status = models.CharField(max_length=50, default="pending")
    interview_date = models.CharField(max_length=150, default="")
    interview_time = models.CharField(max_length=150, default="")
    interview_location_url = models.CharField(max_length=1000)
    interview_online = models.CharField(max_length=150, default="false")

    class Meta:
        db_table = 'Application'


class JobNotification(models.Model):
    job_application = models.ForeignKey('Application', on_delete=models.CASCADE, default=1)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1)
    check_value = models.CharField(max_length=50, default="uncheck")
    time_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Job Notification'


class Chat(models.Model):
    user = models.ManyToManyField('Profile', default=[0], related_name="chat_user_list")
    latest_update = models.CharField(max_length=50, default="none")

    class Meta:
        db_table = 'Chat'


# chat messages
class Chatmessage(models.Model):
    sender = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1, related_name="chat_sender")
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, default=1,)
    message = models.TextField(max_length=3000, default=None)
    time_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Chat Message'


# chat Report
class ChatReported(models.Model):
    reporting_user = models.ForeignKey('Profile', on_delete=models.CASCADE, default=1, related_name="report_sender")
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, default=1,)
    time_reported = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Chat Reported'
