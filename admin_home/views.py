from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth import models
from admin_home.models import Product_Details
from home.models import Registration
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect
from . import views
from customer_home.models import Order,Order_Details
from home.views import send_email
import datetime
from customer_home.models import ReceivedProduct
from home.models import Registration


def index(request):
   userdict={}
   try:
      userdict['id']=request.COOKIES['user_id']
      us = Registration.objects.filter(user_id=userdict['id']).first()
      if(us is not None):
         if(us.role=="admin"):
            return render(request,'admin_home/homepage.html',userdict)
         else:
            return HttpResponseRedirect('/buy')
      else:
         return HttpResponseRedirect('/login')
   except:
      return HttpResponseRedirect('/login')
      # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def addProduct(request):
   userdict={}
   try:
      userdict['id']=request.COOKIES['user_id']
      us = Registration.objects.filter(user_id=userdict['id']).first()

      if(us is not None):
         if(us.role=="admin"):
            if request.method=='GET':
               return render(request,'admin_home/addProduct.html')
            else:
               p=Product_Details()
               p.product_name =request.POST.get('product_name')
               p.price =request.POST.get('product_price')
               p.description =request.POST.get('product_description')
               p.category =request.POST.get('product_category')
               p.product_date=datetime.date.today()
               p.image=request.FILES['image']
               p.save()
               pth='/ad/admin_indexPage'
               return HttpResponseRedirect(pth)
         else:
            return HttpResponseRedirect('/buy')
      else:
         return HttpResponseRedirect('/login')

   except:
      return HttpResponseRedirect('/login')


def deleteProduct(request,slug):
   userdict={}
   try:
      userdict['id']=request.COOKIES['user_id']
      us = Registration.objects.filter(user_id=userdict['id']).first()

      if(us is not None):
         if(us.role=="admin"):
            Product_Details.objects.filter(product_id=slug).delete()
            pth='/viewProduct'
            return HttpResponseRedirect(pth)
         else:
            return HttpResponseRedirect('/buy')
      else:
         return HttpResponseRedirect('/login')

   except:
      return HttpResponseRedirect('/login')
   

def updateProduct(request,slug):
   userdict={}
   try:
      userdict['id']=request.COOKIES['user_id']
      us = Registration.objects.filter(user_id=userdict['id']).first()

      if(us is not None):
         if(us.role=="admin"):
               if request.method=='GET':
                  p=Product_Details.objects.filter(product_id=slug)[0]
                  userdict={}
                  userdict['product_id']=p.product_id
                  userdict['name']=p.product_name
                  userdict['category']=p.category
                  userdict['price']=p.price
                  userdict['description']=p.description
                  return render(request,'admin_home/updateProduct.html',userdict)
               else:
                  name=request.POST.get('product_name')
                  price=request.POST.get('product_price')
                  description=request.POST.get('product_description')
                  category=request.POST.get('product_category')
                  p=Product_Details.objects.filter(product_id=slug).update(product_name=name)
                  p=Product_Details.objects.filter(product_id=slug).update(price=price)
                  p=Product_Details.objects.filter(product_id=slug).update(category=category)
                  p=Product_Details.objects.filter(product_id=slug).update(description=description)
                  pth='/viewProduct'
                  return HttpResponseRedirect(pth)
         else:
            return HttpResponseRedirect('/buy')
      else:
         return HttpResponseRedirect('/login')

   except:
      return HttpResponseRedirect('/login')

def viewProduct(request):
   products=Product_Details.objects.all()
   userdict={}
   userdict['id']=request.COOKIES['user_id']
   userdict['product']=products
   return render(request,'admin_home/viewProduct.html',userdict)

def signout(request):
   response=HttpResponseRedirect('/')
   del request.session['order_confirmation']
   del request.session['success_message']
   response.delete_cookie('user_id')
   return response

def updateProfile(request):
   try:
      if request.method=='GET':
         uid=request.COOKIES['user_id']
         p=Registration.objects.filter(user_id=uid)[0]
         userdict={}
         userdict['id']=p.user_id
         userdict['name']=p.name
         userdict['password']=p.password
         userdict['dob']=p.dob
         userdict['email']=p.email
         userdict['address']=p.address
         userdict['phone']=p.phone
         return render(request,'admin_home/updateProfile.html',userdict)
      else:
         uid=request.COOKIES['user_id']
         r=Registration.objects.filter(user_id=uid)[0]
         name=request.POST.get('name')
         password=request.POST.get('password')
         dob=request.POST.get('dob')
         email=request.POST.get('email')
         address=request.POST.get('address')
         phone=request.POST.get('phn')
         Registration.objects.filter(user_id=uid).update(name=name)
         Registration.objects.filter(user_id=uid).update(password=password)
         Registration.objects.filter(user_id=uid).update(email=email)
         Registration.objects.filter(user_id=uid).update(address=address)
         Registration.objects.filter(user_id=uid).update(phone=phone)
         Registration.objects.filter(user_id=uid).update(name=name)
         Registration.objects.filter(user_id=uid).update(password=password)
         if r.role=='customer':
            pth='/customer_home_index'
         else :
            pth='/ad/admin_indexPage'
         return HttpResponseRedirect(pth)
   except:
      return HttpResponseRedirect('/login')

def addAdmin(request):
   if request.method=='GET':
      return render(request,'admin_home/registration.html')
   if request.POST.get('name') and request.POST.get('password'):
        saverecord = Registration()
        saverecord.name = request.POST.get('name')
        saverecord.password = request.POST.get('password')
        saverecord.dob = request.POST.get('dob')
        saverecord.email = request.POST.get('email')
        saverecord.address = request.POST.get('address')
        saverecord.phone = request.POST.get('phn')
        saverecord.role="admin"
        saverecord.save()
        pth='/ad/admin_indexPage'
        return HttpResponseRedirect(pth)

def viewReceivedProduct(request):   
   products = ReceivedProduct.objects.all()
   return render(request,'admin_home/viewRecievedProduct.html',{'products':products})

def AcceptProduct(request,slug):
   # rp=ReceivedProduct.objects.filter(id=slug).first()
   rp = ReceivedProduct.objects.filter(id=slug)[0]
   ReceivedProduct.objects.filter(id=slug).delete()
   cnt='Your request to sell Product With us, After viewing Product condition and price configuration we decided to buy it.You will get Your payment whenever we will recived product from you.'
   # print(rp)
   send_email(request,'Product Confirmation',rp.seller_email,cnt)
   pth='/viewReceivedProduct'
   return HttpResponseRedirect(pth)

def RejectProduct(request,slug):
   rp=ReceivedProduct.objects.filter(id=slug).first()
   ReceivedProduct.objects.filter(id=slug).delete()
   cnt='We are sorry to say that we can not buy this product from you. looking forward for better Product.'
   send_email(request,'Product Rejection',rp.seller_email,cnt)
   pth='/viewReceivedProduct'
   return HttpResponseRedirect(pth)

def ViewOrder(request):
   orders = Order.objects.all()
   odrs = {}
   for order in orders:
      user = Registration.objects.filter(user_id=order.user_id.user_id).first()
      odrs[order] = user
   return render(request,'admin_home/viewOrder.html',{'orders':odrs})

def ViewDetails(request,slug):
   order = Order.objects.filter(order_id=slug).first()
   order_detail = Order_Details.objects.filter(order_id_id=order)
   user = Registration.objects.filter(user_id = order.user_id.user_id).first()
   context = {}
   for odr in order_detail:
      context[odr] = Product_Details.objects.filter(product_id = odr.product_id.product_id).first()
   return render(request, 'admin_home/viewOrderDetails.html',{'order':context,'user':user,'odr':order})

def MakeDone(request, slug):
   order = Order.objects.filter(order_id=slug).first()
   user = Registration.objects.filter(user_id = order.user_id.user_id).first()
   Order.objects.filter(order_id=slug).update(status='Done')
   cnt='Your recent order on Old-One has been confirmed\n\nOrder Status=Confirmed'
   send_email(request,'Product Rejection',user.email,cnt)
   
   return HttpResponseRedirect('/viewOrder')