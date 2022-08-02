from urllib import response
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template.context_processors import csrf
from requests import session
from home.models import Registration
from customer_home.models import Cart
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from . import views
import random
from django.conf import settings
import smtplib
from email.message import EmailMessage

def index(request):
    return render(request,'home/index.html')

def login(request):
    return render(request,'home/login.html')

def auth_view(request):
    email=request.POST.get('email_id')
    password=request.POST.get('password')    
    us=Registration.objects.filter(email=email,password=password).first()
    if us is not None:
        request.session['order_confirmation']=""
        request.session['success_message']=""
        if (us.role=="Admin" or us.role=="admin") :
            # if us.otp=='none':
            #     context={'message':'Please Verify Your email-id first....'}
            #     return render(request,'home/registration.html',context)
            pth='ad/admin_indexPage'
            
            response = HttpResponseRedirect(pth)
            response.set_cookie("user_id", us.user_id)
            
            return response
        elif us.role=="customer" :
            # if us.otp=='none':
            #     context={'message':'Please Verify Your email-id first....'}
            #     return render(request,'home/registration.html',context)
            pth='customer_home_index'
            response = HttpResponseRedirect(pth)
            response.set_cookie("user_id", us.user_id)
            return response
    else:
        context={
                'message':'Your Password or email-id might be wrong.....'
        }
        return render(request,'home/login.html',context)
    return HttpResponseRedirect('/login')

def register(request):
    if request.method=='GET':
        return render(request,'home/registration.html')
    elif request.POST.get('name') and request.POST.get('password'):
        try:
            exit_user=Registration.objects.filter(email=request.POST.get('email')).first()
            if exit_user:
                context={'message':'Email already registered try with different..','class':'danger'}
                return render(request,'home/registration.html',context)
            
            saverecord = Registration()
            saverecord.name = request.POST.get('name')
            saverecord.password = request.POST.get('password')
            saverecord.dob = request.POST.get('dob')
            saverecord.email = request.POST.get('email')
            saverecord.address = request.POST.get('address')
            saverecord.phone = request.POST.get('phn')
            #saverecord.cart_id=0
            saverecord.role="customer"
            saverecord.otp='none'
            saverecord.save()
            c = Cart(customer_id=saverecord)
            c.save()
            # verify(request)
            # return HttpResponseRedirect('/otp')
            return render(request, 'home/login.html')
        except:
            context={'message':'Some internal server error occured !','class':'danger'}
            return render(request, 'home/registration.html', context)
        
    return render(request,'home/registration.html')
def verify(request):
    if request.method=='GET':
        return render(request,'home/verify_email.html')
    else:
        usr=Registration.objects.filter(email=request.POST.get('email')).first()
        if usr is None:
            context={
                'message':'Entered Email is not registered '
            }
            return render(request,'home/login.html',context)
        if usr.otp!='none':
            context={
                'message':'Entered Email id already verified'
            }
            return render(request,'home/login.html',context)
        otp=str(random.randint(99999,999999))
        request.session['email']=request.POST.get('email')
        request.session['otp']=otp
        send_email(request,'Otp Verification',request.POST.get('email'),'Your Otp is:'+otp)
        return HttpResponseRedirect('/otp')

def check_otp(request):
    cur_otp=request.POST.get('otp')
    if cur_otp==request.session['otp']:
        Registration.objects.filter(email=request.session['email']).update(otp=request.session['otp'])
        customer = Registration.objects.filter(email=request.session['email'])[0]

        # c = Cart(customer_id=customer)
        # c.save()
        context={
            'message':'Sucessfull registered now you can login...'
        }
        return render(request,'home/login.html',context)
    else:
        context={'message':'Invalid Otp....'}
        return render(request,'home/otp.html',context)
def send_email(request,subject,email_id,content):
        # msg = EmailMessage()
        # msg.set_content(content)
        fromEmail = 'emailsender277@gmail.com'
        toEmail = email_id
        # msg['Subject'] = subject
        # msg['From'] = fromEmail
        # msg['To'] = toEmail
        # s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # s.login(fromEmail, 'yujlyjvvqnozpkdm')
        send_mail(subject, content, fromEmail, [toEmail], fail_silently=False)
        # s.quit()
        return
def contactUs(request):
    if request.method=='GET':
        return render(request,'home/contactUs.html')
    else:
        name=request.POST.get('name')
        email=request.POST.get('email')
        content=request.POST.get('comment')
        admin=Registration.objects.filter(role='admin')
        content=content+'\n Customer Name:- '+name+' and  Email_id:- '+email
        for a in admin:
            send_email(request,'Feedback From Customer',a.email,content)
        return render(request,'home/index.html',{'feedback':'Your Feedback Sent Successfully!!!. We will reply as quick as possible.'})
def forgot(request):
    if request.method=='GET':
        return render(request,'home/forgot.html')
    else:
        us=Registration.objects.filter(email=request.POST.get("email"))
        if us is not None:
            cont='Your Password is:'+Registration.objects.filter(email=request.POST.get("email"))[0].password+'\n if you are not requested for forgot password kindly ignore this.'
            send_email(request,'Reset Password',request.POST.get("email"),cont)
        else:
            context={'message':'Please Provide registered email ...'}
            return render(request,'home/forgot.html',context)
    return HttpResponseRedirect('/login')
def otp(request):
    return render(request,'home/otp.html')
# def loggedin(request):
#     return render(request,'home/loggedin.html', {"full_name":request.user.username})
# def invalidlogin(request):
#     return render(request,'home/invalidlogin.html')
def logout(request):
    response=HttpResponseRedirect('/')
    del request.session['order_confirmation']
    del request.session['success_message']
    response.delete_cookie('user_id')
    return response
def term_condition(request):
    return render(request,'home/term_condition.html')
def about_us(request):
    return render(request,'home/about_us.html')
def contactUs(request):
    return render(request,'home/contactUs.html')
