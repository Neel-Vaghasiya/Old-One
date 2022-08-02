from django.shortcuts import render
from .models import ReceivedProduct, Cart
from home.models import Registration
from admin_home.models import Product_Details
from admin_home import models
from home.views import send_email
from customer_home.models import cart_detail,Order,Order_Details
from django.http import HttpResponseRedirect
from django.db.models import Q
import datetime
# Create your views here.
def customer_home_index(request):
    return HttpResponseRedirect('/buy')

def sellProduct(request):
    if request.method=='GET':
        return render(request,'customer_home/SellProduct.html')
    else:
        p = ReceivedProduct()
        customer = Registration.objects.filter(user_id=request.COOKIES['user_id'])[0]
        p.seller_name = customer.name
        p.seller_email = customer.email
        p.product_name = request.POST.get('product')
        p.description = request.POST.get('description')
        p.price = request.POST.get('price')
        p.images = request.FILES['images']
        p.save()
        request.session['success_message']='Thanks for selling with us. We will Inform you about your response soon...'
        return HttpResponseRedirect('/customer_home_index')

def payment(request):
    cart = Cart.objects.filter(customer_id=request.COOKIES['user_id']).first()
    cart_det= cart_detail.objects.filter(cart_id_id=cart)
    # if not cart_det.exists():
    #     return HttpResponseRedirect('customer_home_index')
    details = {}
    items=0
    total=0
    for c in cart_det:
        product = Product_Details.objects.filter(product_id=c.product_id.product_id)[0]
        details[c.product_id.product_id]=product
        items+=1
        total = total + product.price
    
    context={
        'product':details,
        'items':items,
        'total':total
    }
    return render(request,'customer_home/payment.html',context)

def buy(request):
    message1=""
    message2=""
    if request.session['order_confirmation'] is not None:
        message1=request.session['order_confirmation']
        request.session['order_confirmation']=""
    if request.session['success_message'] is not None:
        message2=request.session['success_message']
        request.session['success_message']=""
    products = Product_Details.objects.all()
    return render(request,'customer_home/homepage.html', {'products': products,'msg1':message1,'msg2':message2})

def cart(request,slug):
    customer = Registration.objects.get(user_id=request.COOKIES['user_id'])
    if customer is None:
        return render(request,'home/index.html')
    crt = Cart.objects.filter(customer_id_id=customer)[0]
    # crt = 1
    crt_det=cart_detail.objects.filter(cart_id_id=crt,product_id=slug).first()
    if crt_det is not None:
        return HttpResponseRedirect('/showCart')
    c = cart_detail()
    c.cart_id = crt
    c.product_id = Product_Details.objects.filter(product_id=slug)[0]
    c.save()
    return HttpResponseRedirect('/showCart')

def search(request):
    qry = request.GET["search"]
    p = Product_Details.objects.filter(Q(product_name__icontains=qry) | Q(description__icontains=qry) | Q(category__icontains=qry))
    result={'products':p,'search':qry}
    return render(request,'customer_home/homepage.html',result)

def read_more(request,slug):
    products = Product_Details.objects.filter(product_id=slug)
    return render(request,'customer_home/description.html', {'products': products})

def showCart(request):
    cart = Cart.objects.filter(customer_id=request.COOKIES['user_id'])
    if len(cart)==0:
        return HttpResponseRedirect('/customer_home_index')
    else:
        cart = cart[0]

    cart_det= cart_detail.objects.filter(cart_id=cart.cart_id)
    details = {}
    items=0
    total=0
    for c in cart_det:
        product = Product_Details.objects.filter(product_id=(c.product_id.product_id))[0]
        details[c.product_id]=product
        items += 1
        total = total + product.price
    context={
        'product':details,
        'items':items,
        'total':total
    }
    return render(request,'customer_home/showCart.html',context)

def remove_from_cart(request,slug):
    crt = Cart.objects.get(customer_id=request.COOKIES['user_id'])
    cart_detail.objects.filter(cart_id=crt.cart_id, product_id=slug).delete()
    return HttpResponseRedirect('/showCart')

def place_order(request):
    cart = Cart.objects.filter(customer_id=request.COOKIES['user_id']).first()
    cart_det= cart_detail.objects.filter(cart_id_id=cart).all()
    odr=Order()
    usr=Registration.objects.filter(user_id=request.COOKIES['user_id']).first()
    odr.user_id=usr
    odr.status='pending'
    odr.order_date=datetime.date.today()
    odr.shipping_address=request.POST.get('address')
    odr.amount=0
    odr.save()
    odr=Order.objects.filter(user_id=request.COOKIES['user_id']).last()
    idx=odr.order_id
    amount=0
    for p in cart_det:
        odr_det=Order_Details()
        odr_det.order_id=odr
        prdt=Product_Details.objects.filter(product_id=p.product_id.product_id)[0]
        odr_det.product_id=prdt
        odr_det.save()
        amount+=prdt.price
        cart_det= cart_detail.objects.filter(product_id=p.product_id).delete()
        Product_Details.objects.filter(product_id=p.product_id.product_id).update(available=False)
    Order.objects.filter(user_id=request.COOKIES['user_id'],order_id=odr.order_id).update(amount=amount)
    send_email(request,'Order Confirmation',usr.email, content = 'Your order on Old-One with following details is confirmed!\n Order Status = '+odr.status+'\nTotal Amount= '+str(amount)+'\nOrder Id= '+str(odr.order_id))
    request.session['order_confirmation']='Your Order Placed Successfully'
    return HttpResponseRedirect('customer_home_index')
    
def ViewOrderHistory(request):
   orders = Order.objects.filter(user_id=request.COOKIES['user_id']).all()
   return render(request,'customer_home/viewOrder.html',{'orders':orders})

def ViewOrderHistoryDetails(request,slug):
   order = Order.objects.filter(order_id=slug).first()
   order_detail = Order_Details.objects.all().filter(order_id_id=order)
   user = Registration.objects.filter(user_id = order.user_id.user_id).first()
   context = {}
   for odr in order_detail:
      context[odr] = Product_Details.objects.filter(product_id = odr.product_id.product_id).first()
   return render(request, 'customer_home/viewOrderDetails.html',{'order':context,'user':user,'odr':order})
    
    
    






