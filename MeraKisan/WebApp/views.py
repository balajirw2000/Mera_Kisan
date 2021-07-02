from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib import auth
from cv2 import cv2
import numpy as np
from pyzbar.pyzbar import decode
from .aadhaar import AadhaarSecureQr
import requests
import urllib.parse
import math
import smtplib
import calendar
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import os
import datetime


# Create your views here.
def home(request):
    return render(request, 'WebApp/Home.html')

def contact(request):
    return render(request, 'WebApp/contact.html')

def our_value(request):
    return render(request, 'WebApp/our_value.html')

def DigitalPlatform(request):
    return render(request, 'WebApp/DigitalPlatform.html')

def add1(request):
    return render(request, 'add.html')

def Prodadd(request):
    return render(request, 'Prodadd.html')


def checkout(request):
    return render(request, 'checkout.html')

def aadharveri(request):
    if request.method == "POST":
        file = request.FILES['file']

        i = file.name.rindex(".")
        exten = file.name[i:]
        newname = "x" + exten
        file_save = default_storage.save(newname, file)

        try:
            img = cv2.imread('E:/Mera_Kisan/MeraKisan/media/'+newname)
            for barcode in decode(img):
                x = barcode.data
            obj = AadhaarSecureQr(int(x.decode(encoding='UTF-8')))
            data = obj.decodeddata()
            name = data["name"]
            email = data["email"]
            digit = data["adhaar_last_4_digit"]
            x = {"name": name, "email": email, "digi": digit}
            return render(request, "register.html", x)
        except:
            print("Not valid")
    return render(request, "signup1.html")

def About(request):
    return render(request, 'WebApp/About.html')


