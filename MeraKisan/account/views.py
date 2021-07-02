import random

from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.sessions import serializers
from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pip._vendor import requests
from django.core import serializers
from django.core.serializers import serialize
from django.http import HttpResponse

from .models import Mobile
from .models import *
from django.forms.models import model_to_dict


# Create your views here.
def send_otp(number, otp):
    from twilio.rest import Client

    account_sid = 'Your_account_sid'
    auth_token = 'Your_AUTH_token'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body='You have Successfully Registered in Mera Kisan '
             'Your Otp is'+otp,
        from_='+**********',
        to ='+91'+number,

    )

    print(message.sid)


def login(request, self=type):
    if request.method == 'POST':
        uname = request.POST['Username']
        password = request.POST['Password']
        user = auth.authenticate(username=uname, password=password)
        if user is not None:
            auth.login(request, user)
            # typec = Type.objects.get(type='Customer',username=uname)
            # if typec:
            #     request.session['typec'] = typec
            # else:
            #     typef = Type.objects.get(type='Farmer')
            #     if typef:
            #         request.session['typef']=typef
            return redirect('/')
        else:
            messages.info(request, 'invaild credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST['Name']
        email = request.POST['Email']
        uname = request.POST['Username']
        number = request.POST['number']
        password1 = request.POST['Password1']
        password2 = request.POST['Password2']
        type = request.POST['type']
        if password1==password2:
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            else:
                check_user= User.objects.filter(email=email).first()
                check_profile=OTP.objects.filter(mobile=number).first()
                if check_user or check_profile:
                    context = {'message': 'User already exist', 'class': 'danger'}
                    return render(request, 'register.html', context)
                else:

                    phone_number = Mobile(phonenumber=number, username=uname)
                    phone_number.save();
                    user = User.objects.create_user(first_name=fname, email=email, username=uname,
                                                password=password1)

                    types = Type(user=user, mobile=number, type=type)
                    profile = OTP(user=user, mobile=number, otp="")
                    user.save();
                    profile.save();
                    types.save();

                    return redirect('login')

        else:
            messages.info(request, 'Password does not match')
            return redirect('register')

    else:
        return render(request, 'register.html')


def registerc(request):
    if request.method == 'POST':
        name = request.POST['Name']
        email = request.POST['Email']
        uname = request.POST['Username']
        number = request.POST['number']
        password1 = request.POST['Password1']
        password2 = request.POST['Password2']
        type = request.POST['type']

        if password1==password2:
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'Username Taken')
                return redirect('registerc')
            else:

                phone_number = Mobile(phonenumber=number,username=uname)
                phone_number.save();


                check_user= User.objects.filter(email=email).first()
                check_profile=OTP.objects.filter(mobile=number).first()
                if check_user or check_profile:
                    context = {'message': 'User already exist', 'class': 'danger'}
                    return render(request, 'registerc.html', context)
                else:

                    phone_number = Mobile(phonenumber=number, username=uname)
                    phone_number.save();
                    user = User.objects.create_user(first_name=name, email=email, username=uname,
                                                    password=password1)
                    otp = str(random.randint(1000, 9999))
                    types = Type(user=user, mobile=number, type=type)
                    profile = OTP(user=user, mobile=number, otp=otp)
                    user.save();
                    profile.save();
                    types.save();
                    send_otp(number, otp)
                    request.session['mobile'] = number
                    print('user_created')
                    print(types)
                    return redirect('otp')

        else:
            messages.info(request, 'Password does not match')
            return redirect('registerc')

    else:
        return render(request, 'registerc.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = OTP.objects.filter(mobile=mobile).first()

        if otp == profile.otp:
            return redirect('login')
        else:
            print('Wrong')

            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': mobile}
            return render(request, 'mobile_check.html', context)

    return render(request, 'mobile_check.html', context)
