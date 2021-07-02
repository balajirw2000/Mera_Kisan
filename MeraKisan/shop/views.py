from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from django.template import Context
from django.contrib.auth.models import User
from twilio.rest import Client
from datetime import datetime
import json
# Create your views here.
def add1(request):
    if request.method=='POST':
        username = request.POST['username']
        print(username)
        #user = auth.authenticate(username=username)
        product_name = request.POST['product_name']
        product_variety = request.POST['product_variety']
        quantity=request.POST['quantity']
        value = request.POST['value']
        city_name = request.POST['city_name']
        section = request.POST['section']
        price = request.POST['price']
        price_value = request.POST['price_value']
        image = request.FILES['image']
        #if user is not None:
        add = Addproducts(username=username,product_name=product_name,product_variety=product_variety,quantity=quantity,
                              value=value, city_name=city_name, section=section, price=price, price_value=price_value,image=image)
        add.save();
        return render(request, 'Prodadd.html')
        #else:
        #messages.info(request, 'invaild username')
        #return redirect('add')
    else:
        return render(request, 'add.html')


def ShopNow(request):
    shop_now = Addproducts.objects.all()
    # types = Type.objects.all()
    return render(request, 'ShopNow.html',{'shop_now' : shop_now})

def checkout(request):
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')
        order = Orders(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save();
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save();
        message = render_to_string('mail.html', {'orders': order})
        msg = EmailMessage(
            'MeraKisan',
            message,
            settings.EMAIL_HOST_USER,
            [order.email, ],
        )
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        print("Mail successfully sent")

        account_sid = 'AC4eb065101d67c8b96b29879b03b70a16'
        auth_token = '44357165973b9a8df29f7bf04bebdc72'
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body='You have got an order having order id ' + str(order.order_id) + ' from ' + name +
                 ' email id: ' + email +
                 ' Address :' + address +
                 ' Phone number: ' + phone,

            from_='+14847200081',
            to='+91' + phone,

        )

        print(message.sid)

        thank=True
        id=order.order_id
        return render(request, 'checkout.html', {'thank':thank, 'id':id})
    return render(request, 'checkout.html')

def tracker(request):
    if request.method=="POST":
        orderId= request.POST.get('orderId', '')
        email=request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId , email=email)
            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=orderId)
                updates= []
                for item in update:
                    myDate = datetime.now()
                    formatedDate = myDate.strftime("%d-%B-%Y %H:%M:%S")
                    updates.append({'text':item.update_desc, 'time': formatedDate})
                    response = json.dumps([updates, order[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            #System.out.println(f'exception {e}')
            return HttpResponse('{}')

    return render(request, 'tracker.html')

def viewDetail(request,myid):
    commentsss = AddComments.objects.all()
    #pr_id = AddComments.objects.filter('pr_id')
    #pr_str = str(pr_id)
    shops = Addproducts.objects.filter(id=myid)
    shop_now = Addproducts.objects.all()
    replys = Reply.objects.all()
    #context ={'shops': shops, 'comments': comments ,'pr_id' : pr_id}
    print(shops)
    return render(request, 'ViewDetail.html', {'shops': shops, 'shop_now': shop_now, 'commentsss': commentsss, 'replys':replys})


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        pr_id = request.POST.get('pr_id')
        #reply_id = request.POST.get('reply_id')
        product = Addproducts.objects.get(id=pr_id)
        #reply = Reply(comment=comment, user=user, product=product, pr_id=pr_id, reply_id=reply_id)
        comment = AddComments(comment=comment, user=user, product=product, pr_id=pr_id)
     #   reply.save();
        comment.save();
        messages.success(request, "Your comment has been posted successfully")
        shops = Addproducts.objects.filter(id=pr_id)
        shop_now = Addproducts.objects.all()
        replys = Reply.objects.all()
        commentsss = AddComments.objects.all()
        return render(request, 'ViewDetail.html', {'shops': shops, 'shop_now': shop_now, 'commentsss': commentsss,'replys': replys})


def replyComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        pr_id = request.POST.get('pr_id')
        product = Addproducts.objects.get(id=pr_id)
        reply_id = request.POST.get('reply_id')
        replys = Reply.objects.all()
        shops = Addproducts.objects.filter(id=pr_id)
        shop_now = Addproducts.objects.all()
        commentsss = AddComments.objects.all()
        reply = Reply(comment=comment, user=user, product=product, pr_id=pr_id, reply_id=reply_id)
        reply.save();
        messages.success(request, "Your comment has been posted successfully")
        return render(request, 'ViewDetail.html', {'shops': shops, 'shop_now': shop_now, 'replys': replys,'commentsss':commentsss})



'''def postComment(request):
    if request.method=="POST":
        comment = request.POST.get('comment')
        user = request.user
        comid = request.POST.get('id')
        comment = Comments(comment=comment, user=user,comid=comid)
        comment.save()
        messages.success(request, "Your comment has been posted successfully")

    else:
        pass
    return redirect("ShopNow1.html");'''