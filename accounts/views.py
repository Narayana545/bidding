from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from items.models import Item
from .models import Detail
from django.core.mail import send_mail
from datetime import date
from django.conf import settings
from django.http import JsonResponse
import paypalrestsdk
import datetime
# Create your views here.
def login(request):
    if request.method == 'POST':
        uname = request.POST.get('un','')
        pass1 = request.POST.get('pa','')
        user = auth.authenticate(username=uname,password=pass1)

        if user == None:
            messages.info(request,"invalid username/password")
            return redirect('login')
        else:
            auth.login(request,user)
            return redirect("home")
            
    else:
        return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        name = request.POST['name']
        mail = request.POST['email']
        p1 = request.POST['p1']
        p2 = request.POST['p2']

        contact = request.POST['contact']
        if p1 == p2:
            if User.objects.filter(email=mail).exists():
                messages.info(request,"Already an User with this Email")
                return redirect('register')
            elif User.objects.filter(username=name).exists():
                messages.info(request,"Already an User with this Username")
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=fname,last_name=lname,email=mail,password=p1,username=name)
                user.save()
                obj = Detail(username=name,contact=contact)
                obj.save()
                subject = "Online Bidding"  
                msg     = "Congratulations you are registered successfully."
                to      = mail  
                res     = send_mail(subject, msg, "onlineauction305@gmail.com", [to])
                if res == 1:
                    return redirect('/')
                else:
                    messages.info(request,"Some thing is wrong")
                    return redirect('register')
        else:
            messages.info(request,"Password does not match")
            return redirect('register')
    else:
        return render(request,'register.html')

# @login_required(login_url='login')
# def edit_profile(request):
#     user = request.user  # Get the currently logged-in user
    
#     if request.method == 'POST':
#         user.first_name =request.POST.get('fname')
#         user.last_name =request.POST.get('lname')
#         user.name = request.POST.get('name')                                                  
#         user.email = request.POST.get('email')
#         # Add any other fields here
#         user.save()  # Save the updated user object
#         return redirect('login')  # Redirect to the profile page (adjust URL name as necessary)
    
#     return render(request,'edit_profile.html',{'user': user})

paypalrestsdk.configure({
    'mode': settings.PAYPAL_MODE,  # 'sandbox' or 'live'
    'client_id': settings.PAYPAL_CLIENT_ID,
    'client_secret': settings.PAYPAL_CLIENT_SECRET,
})


@login_required(login_url='login')
def sendMailTowinners(request):
    today = date.today()
    yesterday = today - datetime.timedelta(days=1)
    items = Item.objects.filter(start_date=yesterday, sold="sold", sendwinmail="unsended")

    for i in items:
        try:
            winnerid = i.highest_bidder
            user_obj = User.objects.get(id=winnerid)
            winnermail = user_obj.email
            winuser = user_obj.username

            obj = Detail.objects.get(username=winuser)
            wincon = obj.contact

            itemmail = i.ownermail
            itemUserobj = User.objects.get(email=itemmail)
            itemuser = itemUserobj.username

            obj2 = Detail.objects.get(username=itemuser)
            itemcon = obj2.contact

            payment_amount = str(i.highest_bid)  # Assuming 'highest_bid' is the winning bid amount on the item
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [{
                    "amount": {
                        "total": payment_amount,
                        "currency": "USD"
                    },
                    "description": f"Payment for {i.name}'s auction"
                }],
                "redirect_urls": {
                    "return_url": "http://localhost:8000/execute/",  # Adjust to your actual URL
                    "cancel_url": "http://localhost:8000/cancel/"   # Adjust to your actual URL
                }
            })

            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href

                        # To winner
                        msg = f"Congratulations! You are the winner of the item {i.name}. Please make the payment to complete the transaction. Payment Link: {approval_url}\n\nSeller's Email: {i.ownermail}\nSeller's Contact: {itemcon}\n\nThank you for participating in the auction!"
                        send_email(f"Congratulations! You won {i.name}'s auction!", msg, winnermail)

                        # To owner
                        msg_owner = f"Congratulations! Your item {i.name} has been sold to {winnermail}. Please contact the winner for further details.\n\nWinner's Email: {winnermail}\nWinner's Contact: {wincon}\n\nPayment Link: {approval_url}\n\nThank you!"
                        send_email(f"Your item {i.name} has been sold!", msg_owner, i.ownermail)

            else:
                print("Failed to create PayPal payment link")
                continue  # Skip to the next item

            # Update the item's email status
            i.sendwinmail = "sended"
            i.save()

        except:
            pass

# def create_payment(request):
#     # Logic to create payment (e.g., with PayPal or Stripe)
#     return JsonResponse({'status': 'Payment created successfully'})        

# def execute_payment(request):
#     payment_id = request.GET.get('paymentId')
#     payer_id = request.GET.get('PayerID')
#     payment = paypalrestsdk.Payment.find(payment_id)
    
#     if payment.execute({"payer_id": payer_id}):
#         # Payment executed successfully
#         return render(request, 'execute_payment.html', {'payment_status': 'success', 'transaction_id': payment.transactions[0].related_resources[0].winnerid})
#     else:
#         # Payment failed
#         return render(request, 'execute_payment.html', {'payment_status': 'failed'})

# def cancel_payment(request):
#     return render(request, 'cancel_payment.html')


@login_required(login_url='login')
def pastConfigurations(request):
    # cuser =request.user
    # cmail = cuser.email
    # item = Item.objects.filter(ownermail=cmail)
    item = Item.objects.all()
    for i in item:
        try:
            hb = i.highest_bidder
            if hb is not None:
                i.sold="sold"
                i.save()
            else:
                i.sold="unsold"
                i.save()
        except:
            pass
    # print("hy")

@login_required(login_url='login')
def home(request):
    items = Item.objects.all()
    today = date.today()
    yesterday = today - datetime.timedelta(days=1) 
    # print(today)
    # print(yesterday)    
    for i in items:
        # print (i.start_date)
        if(today > i.start_date):
            i.status = "past"
            # print("past")
        if(today < i.start_date):
            i.status="future"
            # print("future")
        if(today == i.start_date):
            i.status="live"
            # print("live")
        i.save()
        # print("-------")
    pastConfigurations(request)
    sendMailTowinners(request)
    items = Item.objects.filter(status="live")
    return render(request,"home.html",{'items':items})
    
def logout(request):
    auth.logout(request)
    return redirect("login") 

def ilogout(request):
    auth.logout(request)
    return redirect("login") 

@login_required(login_url='login')
def myprofile(request):
    bidder = request.user
    # item_obj = Item.objects.get(highest_bidder=bidder.id)
    details = bidder   
    cuname = details.username
    # print(cuname)
    # ,"item_obj":item_obj
    obj = Detail.objects.filter(username=cuname)
    contact=""
    for i in obj:
        contact = i.contact
    return render(request,"myprofile.html",{"details":details,"contact":contact})

@login_required(login_url='login')
def log(request):
    cuser =request.user
    cmail = cuser.email
    cid = cuser.id
    item_obj = Item.objects.filter(highest_bidder=cid)

    biddeditem = item_obj
    # item = Item.objects.filter(ownermail=cmail)
    pitem = Item.objects.filter(ownermail=cmail).filter(status="past") 
    litem = Item.objects.filter(ownermail=cmail).filter(status="live") 
    fitem = Item.objects.filter(ownermail=cmail).filter(status="future") 
    return render(request,"log.html",{'pitem':pitem,'litem':litem,'fitem':fitem,"biddeditem":biddeditem})

@login_required(login_url='login')
def future(request):
    items = Item.objects.filter(status="future")
    return render(request,"future.html",{"items":items})

@login_required(login_url='login')   
def buy_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if item.sold == "sold":
        messages.error(request, "This item has already been sold.")
        return redirect('item_detail', item_id=item.id)
    
    # Set item as sold and assign the buyer
    item.sold = "sold"
    item.buyer = request.user
    item.save()
    
    # Send a confirmation email to the owner
    if item.sendwinmail == "unsended":
        send_mail(
            subject=f"Your item '{item.name}' has been sold!",
            message=f"Congratulations! Your item '{item.name}' was bought by {request.user.email} for ${item.currentPrice}.",
            from_email="onlineauction305@gmail.com",
            recipient_list=[item.ownermail],
            fail_silently=True
        )
        item.sendwinmail = "sended"
        item.save()

    messages.success(request, f"You bought {item.name} for ${item.currentPrice}")
    return redirect('purchase_success')
