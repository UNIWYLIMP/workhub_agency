import random as ran
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from datetime import datetime


def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


def carrier_advice(request):
    return render(request, "carrier_advice.html")


def employee_signup(request):
    return render(request, 'employee_signup.html')


def employer_signup(request):
    return render(request, 'employer_signup.html')


def signup(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        userType = request.POST['usertype']
        password = request.POST['password']
        password2 = request.POST['repeatpassword']

        if password == password2:
            if User.objects.filter(username=email).exists():
                messages.info(request, 'Email Already In Use')
                if userType == "employee":
                    return redirect('/employee_signup')
                else:
                    return redirect('/employer_signup')

            elif fullname == "":
                messages.info(request, 'Full name can not be empty')
                if userType == "employee":
                    return redirect('/employee_signup')
                else:
                    return redirect('/employer_signup')

            elif email == "":
                messages.info(request, 'Email can not be empty')
                if userType == "employee":
                    return redirect('/employee_signup')
                else:
                    return redirect('/employer_signup')

            elif len(password) < 8:
                messages.info(request, 'password is too short. Try again')
                if userType == "employee":
                    return redirect('/employee_signup')
                else:
                    return redirect('/employer_signup')

            else:
                # create profile
                username = "@" + str(fullname.split(" ")[0]) + str(ran.randint(234564, 4567865564))
                user = User.objects.create_user(username=email, email=username, password=password,
                                                first_name=fullname, last_name="_____")
                user.save()

                profile = Profile(userEmail=email, userName=username, userFullName=fullname, userType=userType,
                                  userPassword=password)
                profile.save()

                admin = Profile.objects.get(userEmail="workhubagency@gmail.com")
                new_chat = Chat()
                new_chat.save()
                new_chat.user.add(profile)
                new_chat.user.add(admin)
                new_chat.save()
                profile.admin_conversation = new_chat.id
                profile.save()
                message = f"Hey {fullname}<br>Welcome onboard to WorkHub Family, here we offer you a chance to rediscover your dream job. Let us get you set on things you need to know in order to use WorkHub platform efficiently and maximize your chance of being chosen.<br><br><br>BRIEFING: <br>As you already know, WorkHub is home to over ten thousands of jobs both hosted and outsourced by employers on our platform. We try to offer the best opportunity to every candidate seeking a job on our platform. WorkHub includes no paid or premium plan, hence guarantying you an equal footing in getting the job just as your fellow job seekers on WorkHub. How then do you stand out to employer? You stand out on this job offers based on merits gotten from experience, education, skills and your resume listed on your profile.<br><br><br>JOB CATEGORY: <br>Under the job sections, jobs are listed based on interests you share. Make use of the search form and filter tab to navigate around thousands of jobs. This features helps narrow your search to your desired job category. <br><br><br> EASY JOB APPLICATION: <br>WorkHub is introducing its newest feature, application by the tap of a button. No lengthy and boring cover letters but your well developed portfolio profile to help you stand out. Note that easy application can only take place when you have your resume uploaded.<br><br><br>NOTIFICATION CATEGORY: <br> Want to know the status of your job applications, have they been accepted, rejected or pending? You can do this here, your notification section helps you keep track of your jobs and upcoming interviews.<br><br><br> CHAT CATEGORY:</br> Want to get in touch with your employer about your upcoming interview? WorkHub platform provides a free real time text base chat feature to do all this. <br><br> In situations of rights violation or verbal slander, ensure to report chat. WorkHub has a team awaiting your call in cases of right violations.<br><br><br>PROFILE CATEGORY:<br> Ensure to build your profile to the best of your capacity, include every education, skill, or experiences. A well built up profile gives you a higher chance of being chosen during application screening.<br><br>"
                new_message = Chatmessage(sender=admin, chat=new_chat, message=message)
                new_message.save()
                login_user = auth.authenticate(username=email, password=password)
                if login_user is not None:
                    auth.login(request, login_user)
                    request.session['userId'] = email
                    return redirect('/dashboard')
                else:
                    print("failed to authenticate")
                    messages.info(request, 'failed to authenticate')
                    request.session['userId'] = email
                    if userType == "employee":
                        return redirect('/employee_signup')
                    else:
                        return redirect('/employer_signup')

        else:
            messages.info(request, 'passwords does not match')
            if userType == "employee":
                return redirect('/employee_signup')
            else:
                return redirect('/employer_signup')

    else:
        return render(request, 'signup.html')


def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['userId'] = email
            return redirect('/dashboard')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('/login')
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect('/login')


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    profile = Profile.objects.get(userEmail=request.session.get('userId'))

    if profile.userType == "employer":
        return redirect('/employer_dashboard')

    elif profile.userType == "employee":
        return redirect('/employee_dashboard')

    else:
        return redirect('/')


def employee_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass
    return render(request, "employee_dashboard.html")


def employee_offers(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    jobs = []
    num_of_jobs = 0

    if request.method == 'GET':
        search_value = request.GET.get('search')
        if search_value == "#$%^&":
            All_Jobs = list(JobPost.objects.all())
            if len(All_Jobs) > 30:
                jobs = ran.sample(All_Jobs, 30)
            else:
                jobs = ran.sample(All_Jobs, len(All_Jobs))
                num_of_jobs = len(jobs)
        else:
            vast = JobPost.objects.filter(job_title__contains=search_value).exists()
            if 3 <= 2:
                pass
            elif vast:
                jobs = list(JobPost.objects.filter(job_title__contains=search_value))
                num_of_jobs = len(jobs)
            else:
                jobs = []
                num_of_jobs = 0
    serialized_jobs = []
    print(jobs)
    for x in jobs:
        requirement_items = list(JobRequirement.objects.filter(job=x))
        requirements = []
        for y in requirement_items:
            requirements.append(str(y.requirement))

        roles_items = list(JobRole.objects.filter(job=x))
        roles = []
        for y in roles_items:
            roles.append(str(y.role))

        categories_items = list(JobCategory.objects.filter(job=x))
        categories = []
        for y in categories_items:
            categories.append(str(y.category_name))

        try:
            profile_picture = x.job_poster.userProfilePicture.url

        except ValueError:
            profile_picture = "none"

        data = {
            "job_id": x.id,
            "job_title": x.job_title,
            "job_description": x.job_description,
            "job_type": str(x.job_type).upper(),
            "job_poster_name": str(x.job_poster.userFullName).upper(),
            "job_poster_email": x.job_poster.userEmail,
            "job_poster_profile_img": profile_picture,
            "job_pay": x.job_pay,
            "job_location": str(x.job_location).upper(),
            "job_requirements": requirements,
            "job_roles": roles,
            "job_categories": categories,
        }
        serialized_jobs.append(data)
    print(serialized_jobs)
    return JsonResponse({"jobs": serialized_jobs, "num_of_jobs": num_of_jobs})


def employee_filter_offers(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    jobs = []
    num_of_jobs = 0

    if request.method == 'GET':
        job_title = request.GET.get('job_title')
        job_country = request.GET.get('job_country')
        job_city = request.GET.get('job_city')
        job_category = request.GET.get('job_category')
        job_company = request.GET.get('job_company')
        job_type = request.GET.get('job_type')
        print("Job Title: ", job_title)
        print("Job Country: ", job_country)
        print("Job City: ", job_city)
        print("Job Category: ", job_category)
        print("Job Company: ", job_company)
        print("Job Type: ", job_type)

        if job_title is None or job_title == "":
            A_stage = list(JobPost.objects.all())
        else:
            start_stage = list(JobPost.objects.all())
            A_stage = []
            for job_post in start_stage:
                if str(job_title).lower() in str(job_post.job_title).lower():
                    A_stage.append(job_post)
                else:
                    pass

        if job_country is None or job_country == "":
            B_stage = A_stage
        else:
            B_stage = []
            for single_job in A_stage:
                if str(job_country).lower() in str(single_job.job_location).lower():
                    B_stage.append(single_job)
                else:
                    pass

        if job_city is None or job_city == "":
            C_stage = B_stage
        else:
            C_stage = []
            for single_job in B_stage:
                if str(job_city).lower() in str(single_job.job_location).lower():
                    C_stage.append(single_job)
                else:
                    pass

        if job_category is None or job_category == "":
            D_stage = C_stage
        else:
            D_stage = []
            for single_job in C_stage:
                categories_set = list(JobCategory.objects.filter(job=single_job))
                for single_category in categories_set:
                    if str(job_category).lower() in str(single_category.category_name).lower():
                        D_stage.append(single_job)
                    else:
                        pass

        if job_company is None or job_company == "":
            E_stage = D_stage
        else:
            E_stage = []
            for single_job in D_stage:
                if str(job_company).lower() in str(single_job.job_poster.userName).lower():
                    E_stage.append(single_job)
                else:
                    pass

        if job_type is None or job_type == "":
            F_stage = E_stage

        elif str(job_type) == "All":
            F_stage = E_stage

        else:
            F_stage = []
            for single_job in E_stage:
                if str(job_type).lower() in str(single_job.job_type).lower():
                    F_stage.append(single_job)
                else:
                    pass
        jobs = F_stage
        num_of_jobs = len(jobs)
    else:
        jobs = []
        num_of_jobs = len(jobs)

    serialized_jobs = []

    for x in jobs:
        requirement_items = list(JobRequirement.objects.filter(job=x))
        requirements = []
        for y in requirement_items:
            requirements.append(str(y.requirement))

        roles_items = list(JobRole.objects.filter(job=x))
        roles = []
        for y in roles_items:
            roles.append(str(y.role))

        categories_items = list(JobCategory.objects.filter(job=x))
        categories = []
        for y in categories_items:
            categories.append(str(y.category_name))

        try:
            profile_picture = x.job_poster.userProfilePicture.url

        except ValueError:
            profile_picture = "none"

        data = {
            "job_id": x.id,
            "job_title": x.job_title,
            "job_description": x.job_description,
            "job_type": x.job_type,
            "job_poster_name": x.job_poster.userFullName,
            "job_poster_email": x.job_poster.userEmail,
            "job_poster_profile_img": profile_picture,
            "job_pay": x.job_pay,
            "job_location": x.job_location,
            "job_requirements": requirements,
            "job_roles": roles,
            "job_categories": categories,
        }

        serialized_jobs.append(data)

    return JsonResponse({"jobs": serialized_jobs, "num_of_jobs": num_of_jobs})


def employee_single_offer(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    job = None
    if request.method == 'GET':
        id_value = request.GET.get('job_id')
        x = JobPost.objects.get(id=id_value)
        requirement_items = list(JobRequirement.objects.filter(job=x))
        requirements = []
        for y in requirement_items:
            requirements.append(str(y.requirement))

        roles_items = list(JobRole.objects.filter(job=x))
        roles = []
        for y in roles_items:
            roles.append(str(y.role))

        categories_items = list(JobCategory.objects.filter(job=x))
        categories = []
        for y in categories_items:
            categories.append(str(y.category_name))

        try:
            profile_picture = x.job_poster.userProfilePicture.url

        except ValueError:
            profile_picture = "none"

        data = {
            "job_id": x.id,
            "job_title": x.job_title,
            "job_description": x.job_description,
            "job_type": x.job_type,
            "job_poster_name": x.job_poster.userFullName,
            "job_poster_email": x.job_poster.userEmail,
            "job_poster_profile_img": profile_picture,
            "job_pay": x.job_pay,
            "job_location": x.job_location,
            "job_requirements": requirements,
            "job_roles": roles,
            "job_categories": categories,
        }
        job = data
    else:
        pass

    return JsonResponse({"job": job})


def employee_process_job_application(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    job = None
    job_external_link = ""
    if request.method == 'GET':
        id_value = request.GET.get('job_id')
        x = JobPost.objects.get(id=id_value)
        try:
            profile_resume = profile.userResume.url
            resume_status = True

        except ValueError:
            profile_resume = "none"
            resume_status = False

        if x.job_external == "true":
            message = "external"
            job_external_link = x.job_external_link

        elif resume_status:
            if Application.objects.filter(job=x,  job_applicant=profile):
                message = "duplicate"
            else:
                newApplication = Application(job=x, job_applicant=profile, application_status="pending", interview_date="",
                                             interview_time="", interview_location_url="", interview_online="")
                newApplication.save()
                message = "true"
        else:
            message = "false"
    else:
        message = "betta"
    return JsonResponse({"message": message, "external_link": job_external_link})


def employee_notifications(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass
    notifications = list(JobNotification.objects.filter(user=profile))
    num_of_notification = len(notifications)
    serialized_notification = []
    for x in notifications:
        hellos = datetime(x.time_sent.year, x.time_sent.month, x.time_sent.day, x.time_sent.hour, x.time_sent.minute,
                          x.time_sent.second)
        tellos = datetime.now()
        timemat = tellos - hellos
        days = timemat.days
        seconds = int(timemat.seconds)
        minutes = int(timemat.seconds / 60)
        if days == 0:
            if minutes - 60 == 0:
                notification_time_sent = f"{int(seconds) - 3600} secs ago"

            elif int(minutes / 60) - 1 == 0:
                notification_time_sent = f"{int(minutes - 60)} mins ago"

            else:
                if int(minutes / 60) - 1 == 25:
                    notification_time_sent = f"1 day ago"
                else:
                    notification_time_sent = f"{int(minutes / 60) - 1} hrs ago"
        elif days < 7:
            notification_time_sent = f"{int(days)} days ago"
        elif 7 <= days <= 30:
            notification_time_sent = f"{int(days / 7)} weeks ago"
        elif 30 < days < 365:
            notification_time_sent = f"{hellos.strftime('%B')} {hellos.strftime('%d')}," \
                                     f" {hellos.strftime('%Y')}"
        elif days > 365:
            notification_time_sent = f"{int(tellos.year - hellos.year)} yrs ago"
        else:
            notification_time_sent = "null"

        data = {
            "notification_id": x.id,
            "message": f"Your application for {x.job_application.job.job_title} under {x.job_application.job.job_poster.userFullName} has been {x.job_application.application_status}",
            "check_value": x.check_value,
            "job_post": x.job_application.job.job_title,
            "job_company": x.job_application.job.job_poster.userFullName,
            "job_company_initial": str(x.job_application.job.job_poster.userFullName)[0].upper(),
            "job_status": x.job_application.application_status,
            "job_location": x.job_application.interview_location_url,
            "interview_date": x.job_application.interview_date,
            "interview_time": x.job_application.interview_time,
            "interview_online": x.job_application.interview_online,
            "time_sent": notification_time_sent
        }

        serialized_notification.append(data)
    updated_serialized_notification = []
    for x in serialized_notification:
        updated_serialized_notification.insert(0, x)

    return JsonResponse({"notifications": updated_serialized_notification, "num_of_notification": num_of_notification})


def employee_view_all_notifications(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    all_user_notifications = JobNotification.objects.filter(user=profile)
    for p in list(all_user_notifications):
        p.check_value = "check"
        p.save()

    return JsonResponse({"message": "success"})


def employee_single_notification(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    notification = None
    if request.method == 'GET':
        id_value = request.GET.get('notification_id')
        x = JobNotification.objects.get(id=id_value)
        x.check_value = "check"
        x.save()
        hellos = datetime(x.time_sent.year, x.time_sent.month, x.time_sent.day, x.time_sent.hour, x.time_sent.minute,
                          x.time_sent.second)
        tellos = datetime.now()
        timemat = tellos - hellos
        days = timemat.days
        seconds = int(timemat.seconds)
        minutes = int(timemat.seconds / 60)
        if days == 0:
            if minutes - 60 == 0:
                notification_time_sent = f"{int(seconds) - 3600} secs ago"

            elif int(minutes / 60) - 1 == 0:
                notification_time_sent = f"{int(minutes - 60)} mins ago"

            else:
                if int(minutes / 60) - 1 == 25:
                    notification_time_sent = f"1 day ago"
                else:
                    notification_time_sent = f"{int(minutes / 60) - 1} hrs ago"
        elif days < 7:
            notification_time_sent = f"{int(days)} days ago"
        elif 7 <= days <= 30:
            notification_time_sent = f"{int(days / 7)} weeks ago"
        elif 30 < days < 365:
            notification_time_sent = f"{hellos.strftime('%B')} {hellos.strftime('%d')}," \
                                     f" {hellos.strftime('%Y')}"
        elif days > 365:
            notification_time_sent = f"{int(tellos.year - hellos.year)} yrs ago"
        else:
            notification_time_sent = "null"

        data = {
            "notification_id": x.id,
            "message": f"Your application for {x.job_application.job.job_title} under {x.job_application.job.job_poster.userFullName} has been {x.job_application.application_status}",
            "check_value": x.check_value,
            "job_post": x.job_application.job.job_title,
            "job_type": x.job_application.job.job_type,
            "job_company": x.job_application.job.job_poster.userFullName,
            "job_company_initial": str(x.job_application.job.job_poster.userFullName)[0].upper(),
            "job_status": x.job_application.application_status,
            "job_location": x.job_application.interview_location_url,
            "interview_date": x.job_application.interview_date,
            "interview_time": x.job_application.interview_time,
            "interview_online": x.job_application.interview_online,
            "time_sent": notification_time_sent
        }
        notification = data
    return JsonResponse({"notification": notification})


def employee_profile(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    userEducation = profile.education_set.all()
    userSkills = profile.skill_set.all()
    userExperience = profile.experience_set.all()
    if len(userSkills) == 0:
        skill = list()
        skill_message = "No Skill Available!"
    else:
        skill = userSkills
        skill_message = "True"
    skills = []
    for z in skill:
        data = {
            "skill_set": z.skill_set,
            "proficiency": z.proficiency,
        }
        skills.append(data)

    if len(userExperience) == 0:
        experience = list()
        experience_message = "No Past Experience Available!"
    else:
        experience = userExperience
        experience_message = "True"
    experiences = []
    for z in experience:
        data = {
            "experience_title": z.Experience_Title,
            "experience_employment_type": z.Experience_Employment_Type,
            "experience_organization_name": z.Experience_Organization_Name,
            "experience_location": z.Experience_Location,
            "experience_description": z.Experience_Description,
            "experience_start_date": z.Experience_Start_Date,
            "experience_close_date": z.Experience_Close_Date,
        }
        experiences.append(data)

    if len(userEducation) == 0:
        education = list()
        education_message = "No Education Available!"
    else:
        education = userEducation
        education_message = "True"
    educations = []
    for z in education:
        data = {
            "school": z.school,
            "degree": z.degree,
            "field": z.field,
            "startDate": z.startDate,
            "endDate": z.endDate,
            "description": z.description
        }
        educations.append(data)
    try:
        profile_picture = profile.userProfilePicture.url

    except ValueError:
        profile_picture = "none"
    return JsonResponse({"profile_email": profile.userEmail, "profile_bio": profile.userBio,
                         "profile_bio_length": len(str(profile.userBio)), "profile_contact":
                             profile.userContact, "profile_name": profile.userFullName,
                         "profile_title": profile.userTitle,
                         "educations": educations, "education_message": education_message, "experiences": experiences,
                         "experience_message": experience_message, "skills": skills, "skill_message": skill_message,
                         "profile_picture": profile_picture, "profile_gender": profile.userGender,
                         "profile_location": profile.userLocation, "profile_birth_date": profile.userDOB})


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    userEducation = profile.education_set.all()
    userSkills = profile.skill_set.all()
    userExperience = profile.experience_set.all()
    if len(userSkills) == 0:
        skill = list()
        skill_message = "No Skill Available!"
    else:
        skill = userSkills
        skill_message = "True"

    if len(userExperience) == 0:
        experience = list()
        experience_message = "No Past Experience Available!"
    else:
        experience = userExperience
        experience_message = "True"

    if len(userEducation) == 0:
        education = list()
        education_message = "No Education Available!"
    else:
        education = userEducation
        education_message = "True"
    print(education)
    try:
        profile_resume = profile.userResume.url

    except ValueError:
        profile_resume = "none"
    return render(request, "edit_profile.html", {"profile": profile, "educations": education, "education_message":
        education_message, "experiences": experience, "experience_message":
                                                     experience_message, "skills": skill,
                                                 "skill_message": skill_message,
                                                 "profile_resume": profile_resume
                                                 })


def editbio(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    if request.method == "POST":
        userContact = request.POST['contact']
        userBio = request.POST['bio']
        userCountry = request.POST['country']
        userCity = request.POST['city']
        userDOB = request.POST['dob']
        userGender = request.POST['gender']

        profile.userBio = userBio
        profile.userContact = userContact
        profile.userLocation = f"{userCity}, {userCountry}"
        profile.userDOB = userDOB
        profile.userGender = userGender
        profile.save()

        return redirect("/edit_profile")

    return render(request, "edit_bio.html")


def addeducation(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    if request.method == "POST":
        school = request.POST["school"]
        degree = request.POST["degree"]
        field = request.POST["field"]
        startDate = request.POST["start"]
        endDate = request.POST["end"]
        description = request.POST["description"]
        newEducation = Education(school=school, degree=degree, field=field, startDate=startDate, endDate=endDate,
                                 description=description, userProfile=profile)
        newEducation.save()
        return redirect("/edit_profile")
    return render(request, "create_education.html")


def addskill(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    if request.method == "POST":
        skill = request.POST['skill']
        proficiency = str(request.POST['proficiency']) + " year(s)"
        new_skill = Skill(skill_set=skill, proficiency=proficiency, userProfile=profile)
        new_skill.save()
        return redirect("/edit_profile")
    return render(request, "create_skill.html")


def addexperience(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')

    if request.method == 'POST':
        experience_title = request.POST['jobtitle']
        experience_description = request.POST['description']
        experience_type = request.POST['employmentType']
        experience_companyName = request.POST['companyName']
        experience_location = request.POST['location']
        experience_start = request.POST['start']
        experience_end = request.POST['end']
        experience_currently = request.POST.get('currentlyWorking', False)

        if str(experience_currently) == 'true':
            experience_end = 'Present'
        else:
            pass

        profile.userTitle = f"{experience_title} at {experience_companyName}"
        new_experience = Experience(Experience_Title=experience_title, Experience_Employment_Type=experience_type,
                                    Experience_Organization_Name=experience_companyName,
                                    Experience_Location=experience_location, Experience_Start_Date=experience_start,
                                    Experience_Close_Date=experience_end, Experience_Description=experience_description,
                                    userProfile=profile)
        new_experience.save()
        profile.save()
        return redirect("/edit_profile")
    return render(request, "create_experience.html")


def deleteeducation(request, value_id):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass
    educationItem = Education.objects.get(id=value_id)
    educationItem.delete()
    return redirect("/edit_profile")


def deleteskill(request, value_id):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    skillItem = Skill.objects.get(id=value_id)
    skillItem.delete()
    return redirect("/edit_profile")


def deleteexperience(request, value_id):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    experienceItem = Experience.objects.get(id=value_id)
    experienceItem.delete()
    return redirect("/edit_profile")


def upload_cv(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    if request.method == "POST":
        cv_file = request.FILES['file']
        profile.userResume = cv_file
        profile.save()

        return redirect("/edit_profile")
    return render(request, "upload_resume.html")


def upload_profile_picture(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if request.method == "POST":
        image_file = request.FILES['image_background']
        profile.userProfilePicture = image_file
        profile.save()

    return redirect("/dashboard")


def employee_chat(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    all_user_chats = Chat.objects.filter(user=profile)
    total = 0
    for e in all_user_chats:
        total += len(list(e.chatmessage_set.all()))
    request.session["total_length_of_chat"] = total

    print(all_user_chats)
    chat_info = []
    chat_info_temporary = []
    for x in list(all_user_chats):
        print(x)
        new_chat_item = {
            "id": x.id,
        }
        for y in list(x.user.all()):
            if y.userEmail != profile.userEmail:
                if profile.userEmail == x.latest_update:
                    new_chat_item["latest_update"] = "new"
                name_List = list(str(y.userFullName))
                name_new = ""
                if len(name_List) > 12:
                    for p in name_List[0:11]:
                        name_new += str(p)
                    name_new += "..."
                else:
                    name_new = y.userFullName
                new_chat_item['friend_name'] = name_new
                try:
                    new_chat_item['friend_profile_img'] = y.userProfilePicture.url
                except ValueError:
                    new_chat_item['friend_profile_img'] = "none"

            else:
                pass

        all_messages_in_a_chat = x.chatmessage_set.all()
        last_message = all_messages_in_a_chat[len(all_messages_in_a_chat) - 1]
        msg = last_message.message
        msg_time_sent = f"{str(last_message.time_sent).split(' ')} {str(last_message.time_sent).split(' ')}"
        hellos = datetime(last_message.time_sent.year, last_message.time_sent.month, last_message.time_sent.day,
                          last_message.time_sent.hour, last_message.time_sent.minute, last_message.time_sent.second)
        tellos = datetime.now()
        timemat = tellos - hellos
        days = timemat.days
        seconds = int(timemat.seconds)
        minutes = int(timemat.seconds / 60)
        if days == 0:
            print(f"yes our {minutes} and seconds {seconds}")
            if minutes - 60 == 0:
                new_chat_item['last_message_time'] = f"{int(seconds) - 3600} secs ago"

            elif int(minutes / 60) - 1 == 0:
                new_chat_item['last_message_time'] = f"{int(minutes - 60)} mins ago"

            else:
                if int(minutes / 60) - 1 == 25:
                    new_chat_item['last_message_time'] = f"1 day ago"
                else:
                    new_chat_item['last_message_time'] = f"{int(minutes / 60) - 1} hrs ago"
        elif days < 7:
            new_chat_item['last_message_time'] = f"{int(days)} days ago"
        elif 7 <= days <= 30:
            new_chat_item['last_message_time'] = f"{int(days / 7)} weeks ago"
        elif 30 < days < 365:
            new_chat_item['last_message_time'] = f"{hellos.strftime('%B')} {hellos.strftime('%d')}," \
                                                 f" {hellos.strftime('%Y')}"
        elif days > 365:
            new_chat_item['last_message_time'] = f"{int(tellos.year - hellos.year)} yrs ago"
        msg_List = list(str(msg))
        message_new = ""
        if len(msg_List) > 12:
            for p in msg_List[0:12]:
                message_new += str(p)
            message_new += "..."
        else:
            message_new = msg
        new_chat_item['last_message'] = message_new
        new_chat_item['time_value'] = seconds
        chat_info_temporary.append(new_chat_item)
    chat_info = sorted(chat_info_temporary, key=lambda j: j['time_value'])
    latest_chat_id = chat_info[0].get("id")
    print(chat_info)
    return JsonResponse({"chat": chat_info, "latest_chat_id": latest_chat_id})


def employee_chat_warn(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    chat_id = request.GET.get("chat_id")
    x_chat = Chat.objects.get(id=chat_id)
    all_chat_user = x_chat.user.all()
    for user in all_chat_user:
        if user.userEmail == profile.userEmail:
            new_report = ChatReported(chat=x_chat, reporting_user=profile)
            new_report.save()
    return JsonResponse({"message": "chat Reported"})


def employee_chat_clear(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    chat_id = request.GET.get("chat_id")
    x_chat = Chat.objects.get(id=chat_id)
    all_chat_user = x_chat.user.all()
    message = "chat not deleted cause not found"
    for user in all_chat_user:
        if user.userEmail == profile.userEmail:
            all_chat_messages = Chatmessage.objects.filter(chat=x_chat)
            for g in all_chat_messages:
                g.delete()
            message = "chat messages cleared successfully"
            new_message = Chatmessage(sender=profile, chat=x_chat, message=message)
            new_message.save()
    return JsonResponse({"message": message})


def employee_chat_delete(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    chat_id = request.GET.get("chat_id")
    x_chat = Chat.objects.get(id=chat_id)
    all_chat_user = x_chat.user.all()
    message = "chat not deleted cause not found"
    for user in all_chat_user:
        if user.userEmail == profile.userEmail:
            x_chat.delete()
            message = "chat deleted successfully"
    return JsonResponse({"message": message})


def employee_private_chat(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    all_user_chats = Chat.objects.filter(user=profile)
    total = 0
    for e in all_user_chats:
        total += len(list(e.chatmessage_set.all()))
    request.session["total_length_of_chat"] = total

    print("point concluded")
    id_chat = request.GET.get("search")
    is_click = request.GET.get("is_click")
    print(f"{id_chat} this is your chat id")
    request.session['private_reload_id'] = id_chat
    private_reload_id = request.session.get('private_reload_id')
    print("this is the private id session", private_reload_id)
    get_chat = Chat.objects.get(id=id_chat)
    if is_click == "true":
        get_chat.latest_update = "none"
        get_chat.save()
    new_profile = profile
    user_set = get_chat.user.all()
    ratter = False
    request.session['private_chat_reload_num'] = 0
    friend_profile_name = ""
    friend_profile_email = ""
    friend_profile_img = ""
    profile_name = ""
    profile_img = ""
    for x in list(user_set):
        if x.id == new_profile.id:
            ratter = True
            profile_name = x.userFullName
            name_List = list(str(profile_name))
            name_new = ""
            if len(name_List) > 18:
                for p in name_List[0:17]:
                    name_new += str(p)
                name_new += "..."
            else:
                name_new = profile_name

            try:
                profile_img = x.userProfilePicture.url

            except ValueError:
                profile_img = "none"
            profile_name = name_new
        else:
            friend_profile_name = x.userFullName
            friend_profile_email = x.userEmail
            friend_name_List = list(str(friend_profile_name))
            friend_name_new = ""
            if len(friend_name_List) > 18:
                for p in friend_name_List[0:17]:
                    friend_name_new += str(p)
                friend_name_new += "..."
            else:
                friend_name_new = friend_profile_name

            try:
                friend_profile_img = x.userProfilePicture.url

            except ValueError:
                friend_profile_img = "none"

            friend_profile_name = friend_name_new
    if not ratter:
        return redirect("/employee_dashboard")
    else:
        pass

    all_messages_in_a_chat = get_chat.chatmessage_set.all()
    request.session["length_of_active_chat"] = len(list(all_messages_in_a_chat))
    list_of_messages = {}
    list_of_messages_id = []
    for message in all_messages_in_a_chat:
        if message.sender.id == new_profile.id:
            sender = "me"
        else:
            sender = "ex"

        try:
            van = list_of_messages[str(message.time_sent.date())]
            if message.time_sent.minute < 10:
                min_str = "0" + str(message.time_sent.minute)
                list_of_messages[str(message.time_sent.date())] += [{"messages": message.message, "time_sent":
                    str(message.time_sent.hour + 1) + ":" +
                    min_str, "sender": sender}]
            else:
                list_of_messages[str(message.time_sent.date())] += [{"messages": message.message, "time_sent":
                    str(message.time_sent.hour + 1) + ":" +
                    str(message.time_sent.minute), "sender": sender}]
        except KeyError:
            if message.time_sent.minute < 10:
                min_str = "0" + str(message.time_sent.minute)
                list_of_messages[str(message.time_sent.date())] = [{"messages": message.message,
                                                                    "time_sent": str(message.time_sent.hour + 1) + ":" +
                                                                                 min_str, "sender": sender}]
            else:
                list_of_messages[str(message.time_sent.date())] = [{"messages": message.message,
                                                                    "time_sent": str(message.time_sent.hour + 1) + ":" +
                                                                                 str(message.time_sent.minute),
                                                                    "sender": sender}]
            list_of_messages_id.append(str(message.time_sent.date()))
    new_digit_list = []
    for x in list_of_messages_id:
        valuations = x.split("-")
        valuation = ""
        for p in valuations:
            valuation += p
        new_digit_list.append(int(valuation))
    new_digit_list.sort()
    list_of_messages_id = []
    for z in new_digit_list:
        list_of_messages_id.append(str(str(z)[0:4] + "-" + str(z)[4:6] + "-" + str(z)[6] + str(z)[-1]))
    print(list_of_messages_id, " this is t")
    print("reached!!!")
    print(list_of_messages, " nal ne mesa")
    print(list_of_messages_id, " nal 22 24ne mesa")
    print(all_messages_in_a_chat[0].time_sent.date(), " this are the message")
    print(f"{get_chat.user.all()} certain chat")
    print(f"{user_set} all user")

    print(profile_name, " n")
    print(profile_img, " i")
    print(friend_profile_img, "f i")
    print(friend_profile_name, " f n")
    print("this is the user email ", friend_profile_email)
    if str(friend_profile_email) == "workhubagency@gmail.com":
        identification_verified = "true"
    else:
        identification_verified = "false"

    return JsonResponse({"user_profile_name": profile_name, "user_profile_pic": profile_img, "friend_profile_pic":
                         friend_profile_img, "friend_profile_name": friend_profile_name, "friend_verification_email":
                         identification_verified, "list_of_messages": list_of_messages, "list_of_messages_id":
                         list_of_messages_id})


def reloadprivatechat(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    id_chat = request.session.get('private_reload_id')

    get_chat = Chat.objects.get(id=id_chat)
    current_chat_length = len(list(get_chat.chatmessage_set.all()))
    active_chat = request.session.get("length_of_active_chat")
    update = "false"
    if current_chat_length > active_chat:
        update = "true"
    return JsonResponse({"update": update})


def reloadprivatechat_two(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    id_chat = request.session.get('private_reload_id')
    all_user_chats = Chat.objects.filter(user=profile)
    total = 0
    for e in all_user_chats:
        total += len(list(e.chatmessage_set.all()))
    total_former = request.session.get("total_length_of_chat")

    reload_chat_list = "false"
    if total > total_former:
        reload_chat_list = "true"

    return JsonResponse({"reload_chat_list": reload_chat_list})


def send_message(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if request.method == "GET":
        message = request.GET.get('new_message')
        new_profile = profile
        id_chat = request.session.get('private_reload_id')
        current_chat = Chat.objects.get(id=id_chat)
        for y in list(current_chat.user.all()):
            if y.userEmail != profile.userEmail:
                current_chat.latest_update = y.userEmail
                current_chat.save()
            else:
                pass
        new_message = Chatmessage(sender=new_profile, chat=current_chat, message=message)
        new_message.save()
    else:
        pass
    return JsonResponse({"value": "message_sent"})


def employer_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    return render(request, "employer_dashboard.html")


def employer_jobs(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass
    try:
        profile_picture = profile.userProfilePicture.url

    except ValueError:
        profile_picture = "none"
    jobs_posted = list(JobPost.objects.filter(job_poster=profile))
    num_of_jobs = len(jobs_posted)
    serialized_jobs = []
    for x in jobs_posted:
        requirement_items = list(JobRequirement.objects.filter(job=x))
        requirements = []
        for y in requirement_items:
            requirements.append(str(y.requirement))

        roles_items = list(JobRole.objects.filter(job=x))
        roles = []
        for y in roles_items:
            roles.append(str(y.role))

        categories_items = list(JobCategory.objects.filter(job=x))
        categories = []
        for y in categories_items:
            categories.append(str(y.category_name))

        try:
            profile_picture = x.job_poster.userProfilePicture.url

        except ValueError:
            profile_picture = "none"

        data = {
            "job_id": x.id,
            "job_title": x.job_title,
            "job_description": x.job_description,
            "job_type": x.job_type,
            "job_poster_name": x.job_poster.userFullName,
            "job_poster_email": x.job_poster.userEmail,
            "job_poster_profile_img": profile_picture,
            "job_pay": x.job_pay,
            "job_location": x.job_location,
            "job_requirements": requirements,
            "job_roles": roles,
            "job_categories": categories,
        }
        serialized_jobs.append(data)

    return JsonResponse({"jobs": serialized_jobs, "num_of_jobs": num_of_jobs})


def employer_single_job(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass

    job = None
    if request.method == 'GET':
        id_value = request.GET.get('job_id')
        x = JobPost.objects.get(id=id_value)
        number_of_applicant = len(list(Application.objects.filter(job=x)))
        requirement_items = list(JobRequirement.objects.filter(job=x))
        requirements = []
        for y in requirement_items:
            requirements.append(str(y.requirement))

        roles_items = list(JobRole.objects.filter(job=x))
        roles = []
        for y in roles_items:
            roles.append(str(y.role))

        categories_items = list(JobCategory.objects.filter(job=x))
        categories = []
        for y in categories_items:
            categories.append(str(y.category_name))

        try:
            profile_picture = x.job_poster.userProfilePicture.url

        except ValueError:
            profile_picture = "none"

        data = {
            "job_id": x.id,
            "job_title": x.job_title,
            "job_description": x.job_description,
            "job_type": x.job_type,
            "job_poster_name": x.job_poster.userFullName,
            "job_poster_email": x.job_poster.userEmail,
            "job_poster_profile_img": profile_picture,
            "job_pay": x.job_pay,
            "job_location": x.job_location,
            "job_requirements": requirements,
            "job_roles": roles,
            "job_categories": categories,
            "number_of_applicant": number_of_applicant,
        }
        job = data
    else:
        pass

    return JsonResponse({"job": job})


def employer_single_job_applicant(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass

    applicant_serialized = []
    job_id = ""
    if request.method == 'GET':
        id_value = request.GET.get('job_id')
        job_id = id_value
        x = JobPost.objects.get(id=id_value)
        number_of_applicant = list(Application.objects.filter(job=x))

        counter = 0
        for z in number_of_applicant:
            try:
                profile_cv = z.job_applicant.userResume.url
                resume_status = "view resume"

            except ValueError:
                profile_cv = "#"
                resume_status = "Cv Unavailable"

            try:
                profile_picture = z.job_applicant.userProfilePicture.url

            except ValueError:
                profile_picture = "none"
            counter += 1
            data = {
                "form_id": counter,
                "applicant_name": z.job_applicant.userFullName,
                "application_id": z.id,
                "applicant_id": z.job_applicant.id,
                "applicant_profile_image": profile_picture,
                "applicant_profile_cv": profile_cv,
                "applicant_profile_cv_status": resume_status,
                "applicant_status": z.application_status,
                "interview_location": "(FILLED)",
                "interview_date": "(FILLED)",
                "interview_time": "(FILLED)",
            }
            applicant_serialized.append(data)

    return JsonResponse({"job_id": job_id, "applicants": applicant_serialized})


def reject_job_application(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass

    if request.method == 'GET':
        job_id = request.GET.get('job_id')
        application_id = request.GET.get('application_id')

        application = Application.objects.get(id=application_id)
        application.application_status = "rejected"
        application.save()

        desired_user = application.job_applicant
        new_notification = JobNotification(job_application=application, user=desired_user, check_value="uncheck")
        new_notification.save()

    return JsonResponse({"message": "success"})


def accept_job_application(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass

    if request.method == 'GET':
        application_id = request.GET.get('application_id')
        location = request.GET.get('location')
        date = request.GET.get('date')
        time = request.GET.get('time')
        online = request.GET.get('online')
        application = Application.objects.get(id=int(application_id))
        application.application_status = "accepted"
        application.interview_date = date
        application.interview_time = time
        application.interview_location_url = location

        if str(online) == "true":
            application.interview_online = "true"
        else:
            application.interview_online = "false"

        application.save()
        all_user_chats = Chat.objects.filter(user=profile)
        create_new_chat = True
        for e in all_user_chats:
            for c in e.user.all():
                if c.userEmail == application.job_applicant.userEmail:
                    new_chat = e
                    new_chat.latest_update = application.job_applicant.userEmail
                    new_chat.save()
                    if application.interview_online == "true":
                        message = f"We are delighted to tell you that your application for {application.job.job_title} under {application.job.job_poster.userFullName} has been {application.application_status}. Your interview would take place on {application.interview_date} at {application.interview_time}, please join the online meeting 10 minutes before the scheduled time to prevent interruptions. <a href'{application.interview_location_url}'>{application.interview_location_url}</a>"
                    else:
                        message = f"We are delighted to tell you that your application for {application.job.job_title} under {application.job.job_poster.userFullName} has been {application.application_status}. Your interview would take place on {application.interview_date} at {application.interview_time}, please ensure to be on time to venue. Interview Location: {application.interview_location_url}"

                    new_message = Chatmessage(sender=profile, chat=new_chat, message=message)
                    new_message.save()
                    create_new_chat = False

        if not create_new_chat:
            pass

        else:
            new_chat = Chat()
            new_chat.save()
            new_chat.user.add(profile)
            new_chat.user.add(application.job_applicant)
            new_chat.save()
            if application.interview_online == "true":
                message = f"We are delighted to tell you that your application for {application.job.job_title} under {application.job.job_poster.userFullName} has been {application.application_status}. Your interview would take place on {application.interview_date} at {application.interview_time}, please join the online meeting 10 minutes before the scheduled time to prevent interruptions. <a href'{application.interview_location_url}'>{application.interview_location_url}</a>"
            else:
                message = f"We are delighted to tell you that your application for {application.job.job_title} under {application.job.job_poster.userFullName} has been {application.application_status}. Your interview would take place on {application.interview_date} at {application.interview_time}, please ensure to be on time to venue. Interview Location: {application.interview_location_url}"

            new_message = Chatmessage(sender=profile, chat=new_chat, message=message)
            new_message.save()

        desired_user = application.job_applicant
        new_notification = JobNotification(job_application=application, user=desired_user, check_value="uncheck")
        new_notification.save()

    return JsonResponse({"message": "success"})


def employer_delete_job(request, id_value):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass

    x = JobPost.objects.get(id=int(id_value))
    x.delete()

    return redirect("/employer_dashboard")


def employer_create_job(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass
    request.session["jobTitle"] = ""
    request.session["jobType"] = ""
    request.session["jobPay"] = ""
    request.session["jobLocation"] = ""
    request.session["jobDescription"] = ""
    request.session["jobRequirements"] = ""
    request.session["jobCategories"] = ""
    request.session["jobExternal"] = "none"
    request.session["jobExternalLink"] = ""

    if request.method == "POST":
        jobTitle = request.POST["jobTitle"]
        print(jobTitle)
        jobType = request.POST["jobType"]
        jobPay = request.POST["jobPay"]
        jobLocation = request.POST["jobLocation"]
        jobDescription = request.POST["jobDescription"]
        try:
            jobExternal = request.POST["jobExternal"]
        except KeyError:
            jobExternal = "none"

        jobExternalLink = request.POST["jobExternalLink"]

        request.session["jobTitle"] = jobTitle
        request.session["jobType"] = jobType
        request.session["jobPay"] = jobPay
        request.session["jobLocation"] = jobLocation
        request.session["jobDescription"] = jobDescription
        request.session["jobExternal"] = jobExternal
        request.session["jobExternalLink"] = jobExternalLink
        return redirect("/create_categories")

    return render(request, "postjob.html")


def create_categories(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass
    print("hello there")
    print(request.session.get("jobTitle"))
    print(len(request.session.get("jobTitle")))
    if not request.session.get("jobTitle", None):
        print("reached")
        return redirect("/employer_create_job")
    if request.method == "GET":
        input_list = request.GET.get("input_bucket")
        print(input_list)
        if input_list is None:
            pass
        else:
            request.session["jobCategories"] = input_list
            return redirect("/create_requirement")
    return render(request, "create_categories.html")


def create_requirement(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass
    if not request.session.get("jobCategories", None):
        print("reached")
        return redirect("/employer_create_job")
    if request.method == "GET":
        input_list = request.GET.get("input_bucket")
        if input_list is None:
            pass
        else:
            request.session["jobRequirements"] = input_list
            return redirect("/create_roles")
    return render(request, "create_requirement.html")


def create_roles(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass
    if not request.session.get("jobRequirements", None):
        print("reached")
        return redirect("/employer_create_job")
    if request.method == "GET":
        input_list = request.GET.get("input_bucket")
        if input_list is None:
            pass
        else:
            roles = request.GET.get("input_bucket")
            requirements = request.session.get("jobRequirements")
            categories = request.session.get("jobCategories")
            job_title = request.session.get("jobTitle")
            job_type = request.session.get("jobType")
            job_pay = request.session.get("jobPay")
            job_location = request.session.get("jobLocation")
            job_description = request.session.get("jobDescription")
            jobExternal = request.session.get("jobExternal")
            jobExternalLink = request.session.get("jobExternalLink")
            new_job = JobPost(job_poster=profile, job_title=job_title, job_type=job_type, job_pay=job_pay,
                              job_location=job_location, job_description=job_description, job_external=jobExternal,
                              job_external_link=jobExternalLink)
            new_job.save()
            update_cart = str(categories).split("$")[:-1]
            update_require = str(requirements).split("$")[:-1]
            update_role = str(roles).split("$")[:-1]
            print(update_cart)
            for x in update_cart:
                new_category = JobCategory(category_name=x)
                new_category.save()
                new_category.job.add(new_job)
                new_category.save()
            for x in update_role:
                new_role = JobRole(role=x, job=new_job)
                new_role.save()
            for x in update_require:
                new_requirement = JobRequirement(requirement=x, job=new_job)
                new_requirement.save()
            return redirect("/dashboard")
    return render(request, "create_roles.html")


def employer_profile(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass

    try:
        profile_picture = profile.userProfilePicture.url

    except ValueError:
        profile_picture = "none"

    return JsonResponse({"profile_email": profile.userEmail, "profile_bio": profile.userBio, "profile_bio_length":
                         len(str(profile.userBio)), "profile_contact": profile.userContact, "profile_name":
                         profile.userFullName, "profile_title": profile.userTitle, "profile_gender": profile.userGender,
                         "profile_location": profile.userLocation, "profile_birth_date": profile.userDOB,
                         "profile_picture": profile_picture})


def employer_edit_profile(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass

    return render(request, "employer_edit_profile.html", {"profile": profile})


def editprofile_employer(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass

    try:
        profile_picture = profile.userProfilePicture.url

    except ValueError:
        profile_picture = "none"

    return render(request, "employer_editprofile", {"profile": profile, "profile_picture": profile_picture})


def employer_editbio(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass

    if request.method == "POST":
        userContact = request.POST['contact']
        userBio = request.POST['bio']
        userCountry = request.POST['country']
        userCity = request.POST['city']
        userDOB = request.POST['dob']
        userGender = request.POST['gender']

        profile.userBio = userBio
        profile.userContact = userContact
        profile.userLocation = f"{userCity}, {userCountry}"
        profile.userDOB = userDOB
        profile.userGender = userGender
        profile.save()

        return redirect("/employer_edit_profile")

    return render(request, "employer_edit_bio.html")


def viewprofile(request, user_id):
    request.session['profile_visit_userId'] = user_id
    return render(request, "viewprofile.html", {"user_id": user_id})


def get_profile(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(id=request.session.get('profile_visit_userId'))
    if profile.userType == "employer":
        return redirect('/employer_dashboard')
    else:
        pass

    userEducation = profile.education_set.all()
    userSkills = profile.skill_set.all()
    userExperience = profile.experience_set.all()
    if len(userSkills) == 0:
        skill = list()
        skill_message = "No Skill Available!"
    else:
        skill = userSkills
        skill_message = "True"
    skills = []
    for z in skill:
        data = {
            "skill_set": z.skill_set,
            "proficiency": z.proficiency,
        }
        skills.append(data)

    if len(userExperience) == 0:
        experience = list()
        experience_message = "No Past Experience Available!"
    else:
        experience = userExperience
        experience_message = "True"
    experiences = []
    for z in experience:
        data = {
            "experience_title": z.Experience_Title,
            "experience_employment_type": z.Experience_Employment_Type,
            "experience_organization_name": z.Experience_Organization_Name,
            "experience_location": z.Experience_Location,
            "experience_description": z.Experience_Description,
            "experience_start_date": z.Experience_Start_Date,
            "experience_close_date": z.Experience_Close_Date,
        }
        experiences.append(data)

    if len(userEducation) == 0:
        education = list()
        education_message = "No Education Available!"
    else:
        education = userEducation
        education_message = "True"
    educations = []
    for z in education:
        data = {
            "school": z.school,
            "degree": z.degree,
            "field": z.field,
            "startDate": z.startDate,
            "endDate": z.endDate,
            "description": z.description
        }
        educations.append(data)
    try:
        profile_picture = profile.userProfilePicture.url

    except ValueError:
        profile_picture = "none"
    return JsonResponse({"profile_email": profile.userEmail, "profile_bio": profile.userBio,
                         "profile_bio_length": len(str(profile.userBio)), "profile_contact":
                             profile.userContact, "profile_name": profile.userFullName,
                         "profile_title": profile.userTitle,
                         "educations": educations, "education_message": education_message, "experiences": experiences,
                         "experience_message": experience_message, "skills": skills, "skill_message": skill_message,
                         "profile_picture": profile_picture, "profile_gender": profile.userGender,
                         "profile_location": profile.userLocation, "profile_birth_date": profile.userDOB,})


def employer_chat(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass
    print("got here")
    all_user_chats = Chat.objects.filter(user=profile)
    total = 0
    for e in all_user_chats:
        total += len(list(e.chatmessage_set.all()))
    request.session["total_length_of_chat"] = total

    print(all_user_chats)
    chat_info = []
    chat_info_temporary = []
    for x in list(all_user_chats):
        print(x)
        new_chat_item = {
            "id": x.id,
        }
        for y in list(x.user.all()):
            if y.userEmail != profile.userEmail:
                if profile.userEmail == x.latest_update:
                    new_chat_item["latest_update"] = "new"
                else:
                    pass

                name_List = list(str(y.userFullName))
                name_new = ""
                if len(name_List) > 12:
                    for p in name_List[0:11]:
                        name_new += str(p)
                    name_new += "..."
                else:
                    name_new = y.userFullName
                new_chat_item['friend_name'] = name_new
                try:
                    new_chat_item['friend_profile_img'] = y.userProfilePicture.url
                except ValueError:
                    new_chat_item['friend_profile_img'] = "none"

            else:
                pass

        all_messages_in_a_chat = x.chatmessage_set.all()
        last_message = all_messages_in_a_chat[len(all_messages_in_a_chat) - 1]
        msg = last_message.message
        msg_time_sent = f"{str(last_message.time_sent).split(' ')} {str(last_message.time_sent).split(' ')}"
        hellos = datetime(last_message.time_sent.year, last_message.time_sent.month, last_message.time_sent.day,
                          last_message.time_sent.hour, last_message.time_sent.minute, last_message.time_sent.second)
        tellos = datetime.now()
        timemat = tellos - hellos
        days = timemat.days
        seconds = int(timemat.seconds)
        minutes = int(timemat.seconds / 60)
        if days == 0:
            print(f"yes our {minutes} and seconds {seconds}")
            if minutes - 60 == 0:
                new_chat_item['last_message_time'] = f"{int(seconds) - 3600} secs ago"

            elif int(minutes / 60) - 1 == 0:
                new_chat_item['last_message_time'] = f"{int(minutes - 60)} mins ago"

            else:
                if int(minutes / 60) - 1 == 25:
                    new_chat_item['last_message_time'] = f"1 day ago"
                else:
                    new_chat_item['last_message_time'] = f"{int(minutes / 60) - 1} hrs ago"
        elif days < 7:
            new_chat_item['last_message_time'] = f"{int(days)} days ago"
        elif 7 <= days <= 30:
            new_chat_item['last_message_time'] = f"{int(days / 7)} weeks ago"
        elif 30 < days < 365:
            new_chat_item['last_message_time'] = f"{hellos.strftime('%B')} {hellos.strftime('%d')}," \
                                                 f" {hellos.strftime('%Y')}"
        elif days > 365:
            new_chat_item['last_message_time'] = f"{int(tellos.year - hellos.year)} yrs ago"
        msg_List = list(str(msg))
        message_new = ""
        if len(msg_List) > 12:
            for p in msg_List[0:12]:
                message_new += str(p)
            message_new += "..."
        else:
            message_new = msg
        new_chat_item['last_message'] = message_new
        new_chat_item['time_value'] = seconds
        chat_info_temporary.append(new_chat_item)
    chat_info = sorted(chat_info_temporary, key=lambda j: j['time_value'])
    latest_chat_id = chat_info[0].get("id")
    print(chat_info)
    return JsonResponse({"chat": chat_info, "latest_chat_id": latest_chat_id})


def employer_private_chat(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass
    all_user_chats = Chat.objects.filter(user=profile)
    total = 0
    for e in all_user_chats:
        total += len(list(e.chatmessage_set.all()))
    request.session["total_length_of_chat"] = total

    print("point concluded")
    id_chat = request.GET.get("search")
    print(f"{id_chat} this is your chat id")
    request.session['private_reload_id'] = id_chat
    private_reload_id = request.session.get('private_reload_id')
    print("this is the private id session", private_reload_id)
    get_chat = Chat.objects.get(id=id_chat)
    get_chat.latest_update = "none"
    get_chat.save()
    new_profile = profile
    user_set = get_chat.user.all()
    ratter = False
    request.session['private_chat_reload_num'] = 0
    friend_profile_name = ""
    friend_profile_img = ""
    profile_name = ""
    profile_img = ""
    for x in list(user_set):
        if x.id == new_profile.id:
            ratter = True
            profile_name = x.userFullName
            name_List = list(str(profile_name))
            name_new = ""
            if len(name_List) > 18:
                for p in name_List[0:17]:
                    name_new += str(p)
                name_new += "..."
            else:
                name_new = profile_name

            try:
                profile_img = x.userProfilePicture.url

            except ValueError:
                profile_img = "none"
            profile_name = name_new
        else:
            friend_profile_name = x.userFullName
            friend_name_List = list(str(friend_profile_name))
            friend_name_new = ""
            if len(friend_name_List) > 18:
                for p in friend_name_List[0:17]:
                    friend_name_new += str(p)
                friend_name_new += "..."
            else:
                friend_name_new = friend_profile_name

            try:
                friend_profile_img = x.userProfilePicture.url

            except ValueError:
                friend_profile_img = "none"

            friend_profile_name = friend_name_new
    if not ratter:
        return redirect("/employer_dashboard")
    else:
        pass

    all_messages_in_a_chat = get_chat.chatmessage_set.all()
    request.session["length_of_active_chat"] = len(list(all_messages_in_a_chat))
    list_of_messages = {}
    list_of_messages_id = []
    for message in all_messages_in_a_chat:
        if message.sender.id == new_profile.id:
            sender = "me"
        else:
            sender = "ex"

        try:
            van = list_of_messages[str(message.time_sent.date())]
            if message.time_sent.minute < 10:
                min_str = "0" + str(message.time_sent.minute)
                list_of_messages[str(message.time_sent.date())] += [{"messages": message.message, "time_sent":
                    str(message.time_sent.hour + 1) + ":" +
                    min_str, "sender": sender}]
            else:
                list_of_messages[str(message.time_sent.date())] += [{"messages": message.message, "time_sent":
                    str(message.time_sent.hour + 1) + ":" +
                    str(message.time_sent.minute), "sender": sender}]
        except KeyError:
            if message.time_sent.minute < 10:
                min_str = "0" + str(message.time_sent.minute)
                list_of_messages[str(message.time_sent.date())] = [{"messages": message.message,
                                                                    "time_sent": str(message.time_sent.hour + 1) + ":" +
                                                                                 min_str, "sender": sender}]
            else:
                list_of_messages[str(message.time_sent.date())] = [{"messages": message.message,
                                                                    "time_sent": str(message.time_sent.hour + 1) + ":" +
                                                                                 str(message.time_sent.minute),
                                                                    "sender": sender}]
            list_of_messages_id.append(str(message.time_sent.date()))
    new_digit_list = []
    for x in list_of_messages_id:
        valuations = x.split("-")
        valuation = ""
        for p in valuations:
            valuation += p
        new_digit_list.append(int(valuation))
    new_digit_list.sort()
    list_of_messages_id = []
    for z in new_digit_list:
        list_of_messages_id.append(str(str(z)[0:4] + "-" + str(z)[4:6] + "-" + str(z)[6] + str(z)[-1]))
    print(list_of_messages_id, " this is t")
    print("reached!!!")
    print(list_of_messages, " nal ne mesa")
    print(list_of_messages_id, " nal 22 24ne mesa")
    print(all_messages_in_a_chat[0].time_sent.date(), " this are the message")
    print(f"{get_chat.user.all()} certain chat")
    print(f"{user_set} all user")

    print(profile_name, " n")
    print(profile_img, " i")
    print(friend_profile_img, "f i")
    print(friend_profile_name, " f n")
    print(list_of_messages_id)
    print(list_of_messages_id)
    return JsonResponse({"user_profile_name": profile_name, "user_profile_pic": profile_img, "friend_profile_pic":
                         friend_profile_img, "friend_profile_name": friend_profile_name, "list_of_messages":
                         list_of_messages, "list_of_messages_id": list_of_messages_id})


def employer_reloadprivatechat(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass
    id_chat = request.session.get('private_reload_id')

    get_chat = Chat.objects.get(id=id_chat)
    current_chat_length = len(list(get_chat.chatmessage_set.all()))
    active_chat = request.session.get("length_of_active_chat")
    update = "false"
    if current_chat_length > active_chat:
        update = "true"
    print('update ', update)
    all_user_chats = Chat.objects.filter(user=profile)
    total = 0
    for e in all_user_chats:
        total += len(list(e.chatmessage_set.all()))
    total_former = request.session.get("total_length_of_chat")

    reload_chat_list = "false"
    if total > total_former:
        reload_chat_list = "true"
    print('update stutus ', reload_chat_list)
    return JsonResponse({"update": update, "reload_chat_list": reload_chat_list})


def employer_send_message(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    else:
        pass

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')
    else:
        pass

    profile = Profile.objects.get(userEmail=request.session.get('userId'))
    if profile.userType == "employee":
        return redirect('/employee_dashboard')
    else:
        pass
    if request.method == "GET":
        message = request.GET.get('new_message')
        new_profile = profile
        id_chat = request.session.get('private_reload_id')
        current_chat = Chat.objects.get(id=id_chat)
        for y in list(current_chat.user.all()):
            if y.userEmail != profile.userEmail:
                current_chat.latest_update = y.userEmail
                current_chat.save()
            else:
                pass
        new_message = Chatmessage(sender=new_profile, chat=current_chat, message=message)
        new_message.save()
    else:
        pass
    return JsonResponse({"value": "message_sent"})
