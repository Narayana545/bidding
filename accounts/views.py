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
        fname = request.POST['fname']
        lname = request.POST['lname']
        name = request.POST['name']
        mail = request.POST['email']
        p1 = request.POST['p1']
        p2 = request.POST['p2']

        if p1 != p2:
            return HttpResponse("Passwords do not match", status=400)

        if len(p1) < 8:
            return HttpResponse("Password must be at least 8 characters long", status=400)

        try:
            user = User.objects.create_user(username=name, email=mail, password=p1)
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.info(request,"Registration successful")
            return redirect("home")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)

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

@login_required
def edit_profile(request):
    # Get the current logged-in user (no need for query as request.user is already the User instance)
    user = request.user
    
    if user:
        if request.method == 'POST':
            # Get new values from the POST request
            fname = request.POST.get('first_name')
            lname = request.POST.get('last_name')
            email = request.POST.get('email')
            
            # Update user fields
            user.first_name = fname
            user.last_name = lname
            user.email = email
            
            # Save the updated user object
            user.save()
            
            # Redirect to home page or any other page after saving
            return redirect('home')
        
        # Render the profile edit page with the current user details
        return render(request, 'edit_profile.html', {'user': user})
    
    # If no user is found (although this is rare, as request.user should always exist if logged in)
    return HttpResponse("No user")

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

            # Update the item's email status
            i.sendwinmail = "sended"
            i.save()

        except:
            pass


@login_required(login_url='login')
def pastConfigurations(request):
    cuser =request.user
    cmail = cuser.email
    item = Item.objects.filter(ownermail=cmail)
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

