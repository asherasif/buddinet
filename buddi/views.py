from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import UserProfile
# Create your views here.

def index(request):
    return render(request,'login.html')

def newsfeed(request):
    # Your existing newsfeed code
    return render(request, 'newsfeed.html')

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                user_profile = UserProfile.objects.create(user=user, email=email, first_name=first_name, last_name=last_name)


        else:
            messages.info(request,"Password Not Matching")
            return redirect('signup')

    return render(request,'signup.html')

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('newsfeed')
        else:
            messages.info(request,'Incorrect Login/Password')
            return render(request,'login.html')
        
    else:
     return render(request,'login.html')