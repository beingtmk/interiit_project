
from django.shortcuts import render, HttpResponse
from django.views import View
from .forms import Sports_Aquatics_Men_form, Sports_Aquatics_Women_form, Sports_Aquatics_Staff_form, Sports_Weightlifting_form, Staff_form, Sports_Athletics_Men_form, Sports_Athletics_Women_form, Sport_All_Common_Games_Men_form, Sport_All_Common_Games_Women_form, Push_Notification_form
from .serializer import Sport_Aquatics_Men_serializer, Sport_Aquatics_Women_serializer, Sport_Aquatics_Staff_serializer,Sport_Weightlifting_serializer, Staff_serializer, Sport_Athletics_Men_serializer, Sport_Athletics_Women_serializer, Sport_All_Common_Games_Men_serializer, Sport_All_Common_Games_Women_serializer
from rest_framework import mixins, viewsets
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sport_Aquatics_Men, Sport_Aquatics_Women, Sport_Aquatics_Staff, Staff, Sport_Weightlifting, Sport_Athletics_Men, Sport_Athletics_Women, Sport_All_Common_Games_Men, Sport_All_Common_Games_Women, debug, Push_Notifications
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.clickjacking import xframe_options_exempt
import json
import time
from .data import Data
from .response_message import response
from django.contrib.auth.decorators import login_required
# Create your views here.

def send_email(user, pwd, recipient, subject, body, instance=None, category=None, sport_name=None, files=None):
    import smtplib
    from os.path import basename
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.utils import COMMASPACE, formatdate

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body
    assert isinstance(TO, list)
    # message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    message = MIMEMultipart(From=FROM, Date=formatdate(localtime=True), Subject=SUBJECT)
    message['subject']=SUBJECT
    message['to']=COMMASPACE.join(TO)
    message.attach(MIMEText(TEXT))
    if files is not None:
        with open(files, 'rb') as fil:
            message.attach(MIMEApplication(fil.read(), Content_Disposition='attachment; filename="%s"'%basename(files), Name=basename(files)))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message.as_string())
        server.close()
        if instance is not None:
            debug_view(instance, category, sport_name, 'YES')
        print('successfully sent the mail')
    except :
        # print(str(error))
        print("failed to send mail")
        if instance is not None:
            debug_view(instance, category, sport_name, 'NO')

def debug_view(instance, category, sport_name, status):
    if category == 'men':
        if sport_name == 'Athletics':
            model = "Sport_Athletics_Men"
        elif sport_name == 'Weightlifting':
            model = "Sport_Weightlifting"
        else:
            model = "Sport_All_Common_Games_Men"
        name = instance.student_name
    elif category == 'women':
        if sport_name == 'Athletics':
            model = "Sport_Athletics_Women"
        else:
            model = "Sport_All_Common_Games_Women"
        name = instance.student_name
    else:
        model = "Staff"
        name = instance.staff_name

    obj = debug(debug_id=instance.pk, model=model, email=instance.email, phone=instance.mobile_no, name=name, mail_status=status)
    obj.save()

class Sports_Register_view(View):
    @xframe_options_exempt
    def get(self, request, sport_name, category, *args, **kwargs):
        form = None
        heading = None
        if sport_name == 'aquatics':
            if category == 'men':
                form = Sports_Aquatics_Men_form
                heading = 'Aquatics Meet Form : Men'
                print('case men')
            elif category == 'women':
                form = Sports_Aquatics_Women_form
                heading = 'Aquatics Meet Form : Women'
                print('case women')
            elif category == 'facultyandstaff':
                form = Sports_Aquatics_Staff_form
                heading = 'Aquatics Meet Form : Faculty and Staff'
                print('case staff')
            else:
                print('Category doesn\'t exist')
        elif sport_name == 'athletics':
            if category == 'men':
                form = Sports_Athletics_Men_form
                heading = '52nd InterIIT Registration : Men'
            elif category == 'women':
                form = Sports_Athletics_Women_form
                heading = '52nd InterIIT Registration : Women'
            elif category == 'facultyandstaff':
                form = Staff_form(initial={'sport_name': sport_name.title()})
                heading = '52nd InterIIT Registration : Faculty and Staff'
            else:
                print('Category doesn\'t exist')
        elif sport_name == 'weightlifting':
            if category == 'men':
                form = Sports_Weightlifting_form
                heading = '52nd InterIIT Registration : Men'
            elif category == 'facultyandstaff':
                form = Staff_form(initial={'sport_name': sport_name.title()})
                heading = '52nd InterIIT Registration : Faculty and Staff'
            else:
                print('Category doesn\'t exist')
        elif sport_name == 'badminton' or sport_name == 'basketball' or sport_name == 'tennis' or sport_name == 'volleyball' or sport_name == 'table_tennis':
            if category == 'men':
                form = Sport_All_Common_Games_Men_form(initial={'sport_name': sport_name.title()})
                heading = '52nd InterIIT Registration : Men'
            elif category == 'women':
                form = Sport_All_Common_Games_Women_form(initial={'sport_name': sport_name.title()})
                heading = '52nd InterIIT Registration : Women'
            elif category == 'facultyandstaff':
                form = Staff_form(initial={'sport_name': sport_name.title()})
                heading = '52nd InterIIT Registration : Faculty and Staff'
            else:
                print('Category doesn\'t exist')
        elif sport_name == 'cricket' or sport_name == 'football' or sport_name == 'hockey' or sport_name == 'squash':
            if category == 'men':
                form = Sport_All_Common_Games_Men_form(initial={'sport_name': sport_name.title()})
                heading = '52nd InterIIT Registration : Men'
            elif category == 'facultyandstaff':
                form = Staff_form(initial={'sport_name': sport_name.title()})
                heading = '52nd InterIIT Registration : Faculty and Staff'
            else:
                print('Category doesn\'t exist')
        else:
            print('Sport doesn\'t exist')
        #print(sport_name, category)
        if sport_name.find("_") > 0:
            passed_sport_name = sport_name.replace("_", " ")
        else:
            passed_sport_name = sport_name
        if form is None:
            return HttpResponse('Registration form doesn\'t exist')
        else:
            return render(request, 'registration-form.html', {'form': form, 'heading': heading, 'sport': passed_sport_name.title()})

    @xframe_options_exempt
    def post(self, request, sport_name, category, *args, **kwargs):
        dictionary = request.POST.dict()
        form = ''
        list = ''
        extra_text = ''
        duplicate = 0
        if sport_name == 'aquatics':
            if category == 'men':
                form = Sports_Aquatics_Men_form(request.POST, request.FILES)
                list = ['free_50m', 'free_100m', 'free_200m', 'free_400m', 'free_1500m', 'back_50m',
                        'back_100m', 'back_200m', 'breast_50m', 'breast_100m', 'breast_200m', 'b_fly_50m', 'b_fly_100m',
                        'i_m_200m']
                extra_text = ', other than water polo and relays'
            elif category == 'women':
                form = Sports_Aquatics_Women_form(request.POST, request.FILES)
                list = ['freestyle_50m', 'freestyle_100m', 'breast_stroke_50m', 'back_stroke_50m', 'butterfly_50m']
                extra_text = ', other than relay'
            elif category == 'facultyandstaff':
                form = Sports_Aquatics_Staff_form(request.POST, request.FILES)
            else:
                print('Category doesn\'t exist')

        elif sport_name == 'athletics':
            if category == 'men':
                form = Sports_Athletics_Men_form(request.POST, request.FILES)
                list = ['_100m', '_200m', '_400m', '_800m', '_1500m', '_5000m', 'hurdles_110m', 'hurdles_400m',
                        'high_jump', 'long_jump', 'triple_jump', 'pole_vault', 'shot_put', 'discuss_throw',
                        'javelin_throw', 'hammer_throw']
                extra_text = ', other than relays'
                queryset = Sport_Athletics_Men.objects.values().filter(email=dictionary['email'],
                                                                       student_name=dictionary['student_name'])
                if len(queryset) > 0:
                    duplicate = 1
            elif category == 'women':
                form = Sports_Athletics_Women_form(request.POST, request.FILES)
                list = ['_100m', '_200m', '_400m', '_800m', '_1500m', 'high_jump', 'long_jump', 'shot_put', 'discuss_throw']
                extra_text = ', other than relays'
                queryset = Sport_Athletics_Women.objects.values().filter(email=dictionary['email'],
                                                                       student_name=dictionary['student_name'])
                if len(queryset) > 0:
                    duplicate = 1
            elif category == 'facultyandstaff':
                request.POST._mutable = True
                request.POST['sport_name'] = sport_name.title()
                form = Staff_form(request.POST, request.FILES)
                queryset = Staff.objects.values().filter(email=dictionary['email'], staff_name=dictionary['staff_name'], sport_name=sport_name.title())
                if len(queryset) > 0:
                    duplicate = 1
            else:
                print('Category doesn\'t exist')

        elif sport_name == 'weightlifting':
            if category == 'men':
                form = Sports_Weightlifting_form(request.POST, request.FILES)
                list = ['upto_56kg', 'upto_62kg', 'upto_69kg', 'upto_77kg', 'above_77kg']
                queryset = Sport_Weightlifting.objects.values().filter(email=dictionary['email'],
                                                         student_name=dictionary['student_name'])
                if len(queryset) > 0:
                    duplicate = 1
            elif category == 'facultyandstaff':
                request.POST._mutable = True
                request.POST['sport_name'] = sport_name.title()
                form = Staff_form(request.POST, request.FILES)
                queryset = Staff.objects.values().filter(email=dictionary['email'],
                                                         staff_name=dictionary['staff_name'],
                                                         sport_name=sport_name.title())
                if len(queryset) > 0:
                    duplicate = 1

        elif sport_name == 'badminton' or sport_name == 'basketball' or sport_name == 'tennis' or sport_name == 'volleyball' or sport_name == 'table_tennis':
            request.POST._mutable = True
            if sport_name.find("_") > 0:
                sport_name = sport_name.replace("_", " ")

            request.POST['sport_name'] = sport_name.title()
            if category == 'men':
                form = Sport_All_Common_Games_Men_form(request.POST, request.FILES)
                queryset = Sport_All_Common_Games_Men.objects.values().filter(email=dictionary['email'],
                                                         student_name=dictionary['student_name'],
                                                         sport_name=sport_name.title())
                if len(queryset) > 0:
                    duplicate = 1
            elif category == 'women':
                form = Sport_All_Common_Games_Women_form(request.POST, request.FILES)
                queryset = Sport_All_Common_Games_Women.objects.values().filter(email=dictionary['email'],
                                                         student_name=dictionary['student_name'],
                                                         sport_name=sport_name.title())
                if len(queryset) > 0:
                    duplicate = 1
            elif category == 'facultyandstaff':
                form = Staff_form(request.POST, request.FILES)
                queryset = Staff.objects.values().filter(email=dictionary['email'],
                                                         staff_name=dictionary['staff_name'],
                                                         sport_name=sport_name.title())
                if len(queryset) > 0:
                    duplicate = 1
            else:
                print('Category doesn\'t exist')

        elif sport_name == 'cricket' or sport_name == 'football' or sport_name == 'hockey' or sport_name == 'squash':
            request.POST._mutable = True
            request.POST['sport_name'] = sport_name.title()
            if category == 'men':
                form = Sport_All_Common_Games_Men_form(request.POST, request.FILES)
                queryset = Sport_All_Common_Games_Men.objects.values().filter(email=dictionary['email'],
                                                         student_name=dictionary['student_name'],
                                                         sport_name=sport_name.title())
                if len(queryset) > 0:
                    duplicate = 1
            elif category == 'facultyandstaff':
                form = Staff_form(request.POST, request.FILES)
                queryset = Staff.objects.values().filter(email=dictionary['email'],
                                                         staff_name=dictionary['staff_name'],
                                                         sport_name=sport_name.title())
                if len(queryset) > 0:
                    duplicate = 1
            else:
                print('Category doesn\'t exist')

        else:
            print('Sport doesn\'t exist')

        if duplicate == 1:
            return render(request, 'registration-response.html', {
                    'message': 'Already Registered.This is not saved.',
                    'duplicate': duplicate
                })
        print('self', self)
        print('request', request.POST)
        print('*args', args)
        count = 0
        if sport_name == 'weightlifting':
            count = count + 1
        # print('**kwargs', **kwargs)
        for item in list:
            if dictionary[item] == "YES" or dictionary[item] == "RESERVE":
                count = count + 1
        print(count)
        details = ""
        if form.is_valid():
            if category == 'facultyandstaff' or count <= 3:
                print('form is valid')
                form.full_clean()
                formsaved = form.save()
                recepient_email = dictionary['email']
                subject = "Registered Successfully for InterIIT Sports Meet 2017"
                message = response(dict=dictionary, category=category, sport_name=sport_name.title())
                print(message)
                data = Data()
                send_email(data.getid(),data.getpwd(),recepient_email,subject,message, formsaved, category, sport_name.title())
                #send_email(data.getid(),data.getpwd(),data.getrecvid(),subject,message)
                return render(request, 'registration-response.html', {
                    'message': 'Registration completed successfully. You are ready to rock at IIT Madras.',
                    'status': 'success',
                })
            else:
                print('Valid form. More than 3 entries chosen')
                if sport_name == 'weightlifting':
                    msg = 'You can only register for a maximum of two events'+extra_text+'.'
                else:
                    msg = 'You can only register for a maximum of three events' + extra_text + '.'
                return render(request, 'registration-response.html', {
                    'message': msg,
                    'status': 'failed',
                })
        else:
            print('invalid form')
            if count <= 3:
                return render(request, 'registration-response.html', {
                    'message': 'Your registration is not valid. Please enter details correctly',
                    'status': 'failed',
                })
            return render(request, 'registration-response.html', {
                'message': 'You can only register for a maximum of three events'+extra_text+'.',
                'status': 'failed',
            })

class Register_Page(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

import json
from django.contrib.auth.models import User
class push_notification_view(View, User):
    def get(self, request, *args, **kwargs):
        form = Push_Notification_form
        print(request.user)
        # print(User.get_username(), User.get_full_name())
        return render(request, 'push-notification.html', {'form': form, 'status': 'loadform', 'username': request.user})
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        print(data, request.user)
        request.POST._mutable = True
        request.POST['username'] = request.user
        if data['sound'] == 'Yes':
            sound = "default"
        else:
            sound = None

        if data['to'] == 'All':
            recepient = "/topics/msgall"
        else:
            recepient = data['to']
        url = "https://fcm.googleapis.com/fcm/send"
        payload = {
            "notification": {
                "title": data['title'],
                "body": data['message'],
                "sound": sound,
                "click_action": "FCM_PLUGIN_ACTIVITY"
            },
            "data": {
                "page": data['push_page'],
                "message": data['message']
            },
            "to": recepient,
            "priority": "high",
            "restricted_package_name": ""
        }
        headers = {"content-type": "application/json", "authorization": "key=AIzaSyBKggf94MICpd1KcdOTRRbUg6sTDNNJZXc"}
        import requests
        resp = requests.post(url, data=json.dumps(payload), headers=headers)
        print(resp.status_code)
        form = Push_Notification_form(request.POST)
        if resp.status_code == requests.codes.ok:
            resp1 = 'True'
            form.full_clean()
            formsaved = form.save()
            message = "Notification sent successfully."
        else:
            resp1 = 'False'
            message = "Failed to check notification. Please check if all field are filled correctly."
        return render(request, 'push-notification.html', {'status': resp1, 'message': message, 'username': request.user})

def Redirect_To_Register_Page(request):
    return redirect('/sport/register/')

@login_required(login_url='/login/')
def Download_JSON(request):
    if request.method == 'GET':
        return render(request, 'download.html')
def Already_Sent_Notification(request):
    querylist = Push_Notifications.objects.all()
    print(querylist)
    if request.method == 'GET':
        return render(request, 'already-sent-notifications.html', {'querylist': querylist})


class json_aquatics_men(LoginRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = Sport_Aquatics_Men_serializer
    queryset = Sport_Aquatics_Men.objects.all()

class json_aquatics_women(LoginRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = Sport_Aquatics_Women_serializer
    queryset = Sport_Aquatics_Women.objects.all()

class json_aquatics_staff(LoginRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = Sport_Aquatics_Staff_serializer
    queryset = Sport_Aquatics_Staff.objects.all()

class json_weightlifting(LoginRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = Sport_Weightlifting_serializer
    queryset = Sport_Weightlifting.objects.all()

class json_athletics_men(LoginRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = Sport_Athletics_Men_serializer
    queryset = Sport_Athletics_Men.objects.all()

class json_athletics_women(LoginRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = Sport_Athletics_Women_serializer
    queryset = Sport_Athletics_Women.objects.all()

class json_staff(LoginRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = Staff_serializer
    queryset = Staff.objects.all()

class json_sport_all_other_games_men(LoginRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = Sport_All_Common_Games_Men_serializer
    queryset = Sport_All_Common_Games_Men.objects.all()

class json_sport_all_other_games_women(LoginRequiredMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = Sport_All_Common_Games_Women_serializer
    queryset = Sport_All_Common_Games_Women.objects.all()
    
def sendmailtoalreadyregistered_men(id=None):
    listmen = ('iit_name', 'student_name', 'blood_group', 'mobile_no', 'email', 'mode_of_transportation',
               'transport_name', 'arrival_date', 'arrival_time', 'departure_date', 'departure_time', 'food',
               'water_polo', 'free_50m', 'free_100m', 'free_200m', 'free_400m', 'free_1500m', 'back_50m', 'back_100m',
               'back_200m', 'breast_50m', 'breast_100m', 'breast_200m', 'b_fly_50m', 'b_fly_100m', 'i_m_200m',
               'free_relay_4x100m', 'medley_relay_4x100m',)
    n=len(listmen)
    if id is not None:
        queryset = Sport_Aquatics_Men.objects.values().filter(id=id)
    else:
        queryset = Sport_Aquatics_Men.objects.values()

    for object in queryset:
        #print(object, "\n\n\n")
        details = ""
        for i in range(0, n):
            if listmen[i] == 'student_name':
                details += "name : " + str(object[listmen[i]]) + "\n"
            elif listmen[i] == 'iit_name':
                details += str(object[listmen[i]]) + "\n"
            else:
                details += listmen[i]+" : "+str(object[listmen[i]])+"\n"
        #print(details, "\n")
        recepient_name = object['student_name']
        message = '''Dear {}, 
    You have successfully registered for InterIIT Sports Meet 2017.

Details:
{}

In case of any error reply to this mail. Your image is stored in our database.
'''.format(recepient_name, details)
        recepient_email = object['email']
        subject = "Registered Successfully for InterIIT Sports Meet 2017"
        data = Data()
        print(message)
        send_email(data.getid(), data.getpwd(), recepient_email, subject, message)

def sendmailtoalreadyregistered_women(id=None):
    listwomen = ('iit_name', 'student_name', 'blood_group', 'mobile_no', 'email', 'mode_of_transportation',
                 'transport_name', 'arrival_date', 'arrival_time', 'departure_date', 'departure_time', 'food',
                 'freestyle_50m', 'freestyle_100m', 'breast_stroke_50m', 'back_stroke_50m', 'butterfly_50m',
                 'freestyle_relay_4x50m',)
    n=len(listwomen)
    if id is not None:
        queryset = Sport_Aquatics_Women.objects.values().filter(id=id)
    else:
        queryset = Sport_Aquatics_Women.objects.values()

    for object in queryset:
        details = ""
        for i in range(0, n):
            if listwomen[i] == 'student_name':
                details += "name : " + str(object[listwomen[i]]) + "\n"
            elif listwomen[i] == 'iit_name':
                details += str(object[listwomen[i]]) + "\n"
            else:
                details += listwomen[i]+" : "+str(object[listwomen[i]])+"\n"
        recepient_name = object['student_name']
        message = '''Dear {}, 
    You have successfully registered for InterIIT Sports Meet 2017.

Details:
{}

In case of any error reply to this mail. Your image is stored in our database.
'''.format(recepient_name, details)
        recepient_email = object['email']
        subject = "Registered Successfully for InterIIT Sports Meet 2017"
        data = Data()
        print(message)
        send_email(data.getid(), data.getpwd(), recepient_email, subject, message)

def sendmailtoalreadyregistered_facultyandstaff(id=None):
    listfacultyandstaff = ('iit_name', 'staff_name', 'blood_group', 'mobile_no', 'email', 'mode_of_transportation',
              'transport_name', 'arrival_date', 'arrival_time', 'departure_date', 'departure_time', 'food',
              'designation',)
    n=len(listfacultyandstaff)
    if id is not None:
        queryset = Sport_Aquatics_Staff.objects.values().filter(id=id)
    else:
        queryset = Sport_Aquatics_Staff.objects.values()

    for object in queryset:
        details = ""
        for i in range(0, n):
            if listfacultyandstaff[i] == 'staff_name':
                details += "name : " + str(object[listfacultyandstaff[i]]) + "\n"
            elif listfacultyandstaff[i] == 'iit_name':
                details += str(object[listfacultyandstaff[i]]) + "\n"
            else:
                details += listfacultyandstaff[i]+" : "+str(object[listfacultyandstaff[i]])+"\n"
        recepient_name = object['staff_name']
        message = '''Dear {}, 
    You have successfully registered for InterIIT Sports Meet 2017.

Details:
{}

In case of any error reply to this mail. Your image is stored in our database.
'''.format(recepient_name, details)
        recepient_email = object['email']
        subject = "Registered Successfully for InterIIT Sports Meet 2017"
        data = Data()
        print(message)
        send_email(data.getid(), data.getpwd(), recepient_email, subject, message)

def send_mail_to_already_registered():
    sport_name = ""
    list = ""
    queryset = ""

    print("Select Model:\n1. Sport_Athletics_Men\n2. Sport_Athletics_Women\n3. Sport_Weightlifting\n4. Sport_All_Common_Games_Men\n5. Sport_All_Common_Games_Women\n6. Staff\n")
    select_model = input()
    print("1. Send by model data ID\n2. Send to all\n")
    select_send = input()

    id = ""
    if select_send == str(1):
        print("Enter id: ")
        id = input()
    # else:
    #     print("Something wrong.")

    # print("model = {}\nSend = {}\nid = {}".format(select_model, select_send, id))
    if select_model == str(1):
        list = ('iit_name', 'student_name', 'blood_group', 'mobile_no', 'email', 'food',
                              '_100m', '_200m', '_400m', '_800m', '_1500m', '_5000m', 'hurdles_110m', 'hurdles_400m',
                              'high_jump',
                              'long_jump', 'triple_jump', 'pole_vault', 'shot_put', 'discuss_throw', 'javelin_throw',
                              'hammer_throw',
                              'relay_4x100m', 'relay_4x400m',)
        sport_name = 'Athletics'
        if select_send == str(1):
            queryset = Sport_Athletics_Men.objects.values().filter(id=id)
        elif select_send == str(2):
            queryset = Sport_Athletics_Men.objects.values()
        else:
            print("Wrong Input")
    if select_model == str(2):
        list = ('iit_name', 'student_name', 'blood_group', 'mobile_no', 'email', 'food',
                                '_100m', '_200m', '_400m', '_800m', '_1500m', 'high_jump', 'long_jump', 'shot_put',
                                'discuss_throw',
                                'relay_4x100m', 'relay_4x400m',)
        sport_name = 'Athletics'
        if select_send == str(1):
            queryset = Sport_Athletics_Women.objects.values().filter(id=id)
        elif select_send == str(2):
            queryset = Sport_Athletics_Women.objects.values()
        else:
            print("Wrong Input")
    if select_model == str(3):
        list = ('iit_name', 'student_name', 'blood_group', 'mobile_no', 'email', 'food', 'upto_56kg', 'upto_62kg', 'upto_69kg',
              'upto_77kg','above_77kg',)
        sport_name = 'Weightlifting'
        if select_send == str(1):
            queryset = Sport_Weightlifting.objects.values().filter(id=id)
        elif select_send == str(2):
            queryset = Sport_Weightlifting.objects.values()
        else:
            print("Wrong Input")
    if select_model == str(4):
        list = ('iit_name', 'student_name', 'blood_group', 'mobile_no', 'email', 'food',)
        if select_send == str(1):
            queryset = Sport_All_Common_Games_Men.objects.values().filter(id=id)
        elif select_send == str(2):
            queryset = Sport_All_Common_Games_Men.objects.values()
        else:
            print("Wrong Input")
        sport_name = queryset[0]['sport_name']
    if select_model == str(5):
        list = ('iit_name', 'student_name', 'blood_group', 'mobile_no', 'email', 'food',)
        if select_send == str(1):
            queryset = Sport_All_Common_Games_Women.objects.values().filter(id=id)
        elif select_send == str(2):
            queryset = Sport_All_Common_Games_Women.objects.values()
        else:
            print("Wrong Input")
        sport_name = queryset[0]['sport_name']
    if select_model == str(6):
        list = ('iit_name', 'staff_name', 'blood_group', 'mobile_no', 'email', 'food', 'designation',)
        if select_send == str(1):
            queryset = Staff.objects.values().filter(id=id)
        elif select_send == str(2):
            queryset = Staff.objects.values()
        else:
            print("Wrong Input")
        sport_name = queryset[0]['sport_name']

    n = len(list)
    for object in queryset:
        details = ""
        for i in range(0, n):
            if list[i] == 'staff_name' or list[i] == 'student_name':
                details += "name : " + str(object[list[i]]) + "\n"
            elif list[i] == 'iit_name':
                details += str(object[list[i]]) + "\n"
            else:
                details += list[i] + " : " + str(object[list[i]]) + "\n"
        if select_model == str(6):
            recepient_name = object['staff_name']
        else:
            recepient_name = object['student_name']
        message = '''Dear {}, 
    You have successfully registered for InterIIT Sports Meet 2017.

You have registered for {}.

Details:
{}

In case of any error reply to this mail. Your image is stored in our database.
'''.format(recepient_name, sport_name, details)
        recepient_email = object['email']
        subject = "Registered Successfully for InterIIT Sports Meet 2017"
        data = Data()
        print(message)
        send_email(data.getid(), data.getpwd(), recepient_email, subject, message)

email_list = {}
def send_extra_mail():
    for i in range(0, 6):
        if i == 0:
            queryset = Sport_Weightlifting.objects.values()
        elif i == 1:
            queryset = Sport_Athletics_Men.objects.values()
        elif i == 2:
            queryset = Sport_Athletics_Women.objects.values()
        elif i == 3:
            queryset = Sport_All_Common_Games_Men.objects.values()
        elif i == 4:
            queryset = Sport_All_Common_Games_Women.objects.values()
        elif i == 5:
            queryset = Staff.objects.values()
        # j = 0
        for object in queryset:
            if object['email'] in email_list:
                email_list[object['email']] = email_list[object['email']] + 1
            else:
                email_list[object['email']] = 1
            # if j == 10:
            #     break
            # else:
            #     j = j + 1
    #print(email_list)
    email_list_array = ['nitinkumar6912@gmail.com']
    for key in email_list.keys():
        email_list_array.append(key)
    print (email_list_array)
    # arr = ['nitinkumar6912@gmail.com', 'ep14b018@smail.iitm.ac.in']
    subject = "Invitation - Closing Ceremony"
    message = '''23 battalions, 13 battlefields, 9 days of epic rivalry and awe inspiring sportsmanship, and it all comes to a thrilling end. The 52nd Inter IIT Sports Meet was a phenomenal journey. A journey that gave the most fabulous stories. One that made us laugh, cry and bond together as a family, working and practicing day and night, meeting new people. One that left us with memories, tales and experiences that would last unto eternity and beyond. As it winds to a close, join us in crafting a fitting epilogue to this sporting saga. For maybe it was your Game, but it always was Our story. 

We, the 52nd Inter IIT Organizing Committee cordially solicit your esteemed presence at the Closing Ceremony to be held at Manohar C Watsa Stadium at 3 pm today. 

The closing ceremony will also have the trophy distribution for the coveted and tightly fought General Championship, Women's General Championship and so on. Turn up to cheer all the champions. For in trying and persevering and giving it all they've got, everyone is a champion.

One last time, 
Inter IIT Organizing Committee
52nd Inter IIT Sports Meet
IIT Madras
#MADrush

Your Game. Our Story.'''
    data = Data()
    print(data.getid(), data.getpwd(), email_list_array, subject, message, '/home/light/Documents/all_static_items/documents/Closing_Ceremony_Invitation.pdf')
    send_email(data.getid(), data.getpwd(), email_list_array, subject, message, files='/home/light/Documents/all_static_items/documents/Closing_Ceremony_Invitation.pdf')
