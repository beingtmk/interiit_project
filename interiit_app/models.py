from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import os
from datetime import datetime
from django.utils import timezone
# from uuid import uuid4
# Create your models here.

class CommomChoices:
    iitChoices = (
        ('IIT KHARAGPUR', 'IIT Kharagpur'),
        ('IIT BOMBAY', 'IIT Bombay'),
        ('IIT KANPUR', 'IIT Kanpur'),
        ('IIT MADRAS', 'IIT Madras'),
        ('IIT DELHI', 'IIT Delhi'),
        ('IIT GUHAWATI', 'IIT Guhawati'),
        ('IIT ROORKEE', 'IIT Roorkee'),
        ('IIT BHUBANESHWAR', 'IIT Bhubaneshwar'),
        ('IIT GANDHINAGAR', 'IIT Gandhinagar'),
        ('IIT HYDERABAD', 'IIT Hyderabad'),
        ('IIT JODHPUR', 'IIT Jodhpur'),
        ('IIT PATNA', 'IIT Patna'),
        ('IIT ROPAR', 'IIT Ropar'),
        ('IIT INDORE', 'IIT Indore'),
        ('IIT MANDI', 'IIT Mandi'),
        ('IIT (BHU) VARANASI', 'IIT (BHU) Varanasi'),
        ('IIT PALAKKAD', 'IIT Palakkad'),
        ('IIT TIRUPATI', 'IIT Tirupati'),
        ('IIT (ISM) DHANBAD', 'IIT (ISM) Dhanbad'),
        ('IIT BHILAI', 'IIT Bhilai'),
        ('IIT GOA', 'IIT Goa'),
        ('IIT JAMMU', 'IIT Jammu'),
        ('IIT DHARWAD', 'IIT Dharwad'),
    )

    binaryChoices = (
        ('YES', 'Yes'),
        ('NO', 'No'),
    )

    foodChoices = (
        ('VEGETARIAN', 'Vegetarian'),
        ('JAIN', 'Jain'),
        ('NON-VEGETARIAN', 'Non-Vegetarian'),
    )

    genderChoices = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )

    bloodGroupChoices = (
        ('O-', 'O-'),
        ('O+', 'O+'),
        ('A-', 'A-'),
        ('A+', 'A+'),
        ('B-', 'B-'),
        ('B+', 'B+'),
        ('AB-', 'AB-'),
        ('AB+', 'AB+'),
    )
class Sport_Aquatics_Men(models.Model):
    def path_and_rename(instance, filename):
        upload_to = 'AquaticsMeet/Men'
        ext = filename.split('.')[-1]
        namearray = instance.student_name.split(' ')
        namelen = len(namearray)
        name = ''
        for i in range(0, namelen):
            name = name + namearray[i].capitalize()
        filename = '{}_Participant_{}.{}'.format(name, instance.iit_name, ext)
        return os.path.join(upload_to, filename)

    iit_name = models.CharField(max_length=25, choices=CommomChoices.iitChoices)
    student_name = models.CharField(max_length=50)
    blood_group = models.CharField(max_length=5, choices=CommomChoices.bloodGroupChoices)
    mobile_no = PhoneNumberField()
    email = models.EmailField()
    photo = models.ImageField(upload_to=path_and_rename, null=True, default=None)
    arrival = models.CharField(max_length=20)
    arrival_time = models.CharField(max_length=20)
    departure = models.CharField(max_length=20)
    departure_time = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    food = models.CharField(max_length=20, default='VEGETARIAN', choices=CommomChoices.foodChoices)
    water_polo = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    free_50m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    free_100m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    free_200m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    free_400m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    free_1500m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    back_50m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    back_100m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    back_200m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    breast_50m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    breast_100m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    breast_200m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    b_fly_50m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    b_fly_100m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    i_m_200m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    free_relay_4x100m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    medley_relay_4x100m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)

    def __str__(self):
        return_str = '''
            Name : {}
            Blood Group : {}
            Mobile No. : {}
            Email : {}
        '''.format(
            self.student_name,
            self.blood_group,
            self.mobile_no,
            self.email,
        )
        return return_str

class Sport_Aquatics_Women(models.Model):
    def path_and_rename(instance, filename):
        upload_to = 'AquaticsMeet/Women'
        ext = filename.split('.')[-1]
        namearray = instance.student_name.split(' ')
        namelen = len(namearray)
        name = ''
        for i in range(0, namelen):
            name = name + namearray[i].capitalize()
        filename = '{}_Participant_{}.{}'.format(name, instance.iit_name, ext)
        return os.path.join(upload_to, filename)

    iit_name = models.CharField(max_length=25, choices=CommomChoices.iitChoices)
    student_name = models.CharField(max_length=50)
    blood_group = models.CharField(max_length=5, choices=CommomChoices.bloodGroupChoices)
    mobile_no = PhoneNumberField()
    email = models.EmailField()
    photo = models.ImageField(upload_to=path_and_rename, null=True, default=None)
    arrival = models.CharField(max_length=20)
    arrival_time = models.CharField(max_length=20)
    departure = models.CharField(max_length=20)
    departure_time = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    food = models.CharField(max_length=20, default='VEGETARIAN', choices=CommomChoices.foodChoices)
    freestyle_50m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    freestyle_100m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    breast_stroke_50m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    back_stroke_50m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    butterfly_50m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)
    freestyle_relay_4x50m = models.CharField(max_length=10, default='NO', choices=CommomChoices.binaryChoices)

class Sport_Aquatics_Staff(models.Model):
    def path_and_rename(instance, filename):
        upload_to = 'AquaticsMeet/Staff'
        ext = filename.split('.')[-1]
        namearray = instance.staff_name.split(' ')
        namelen = len(namearray)
        name = ''
        for i in range(0, namelen):
            name = name + namearray[i].capitalize()
        filename = '{}_Staff_{}.{}'.format(name, instance.iit_name, ext)
        return os.path.join(upload_to, filename)

    iit_name = models.CharField(max_length=25, choices=CommomChoices.iitChoices)
    staff_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=8, default='MALE', choices=CommomChoices.genderChoices)
    blood_group = models.CharField(max_length=5, choices=CommomChoices.bloodGroupChoices)
    mobile_no = PhoneNumberField()
    email = models.EmailField()
    photo = models.ImageField(upload_to=path_and_rename, null=True, default=None)
    arrival = models.CharField(max_length=20)
    arrival_time = models.CharField(max_length=20)
    departure = models.CharField(max_length=20)
    departure_time = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    food = models.CharField(max_length=20, default='VEGETARIAN', choices=CommomChoices.foodChoices)
    designation = models.CharField(max_length=30)