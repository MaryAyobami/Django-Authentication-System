
from datetime import datetime
from django.shortcuts import redirect, render
from myforms.form import SignUpForm
from django.contrib.auth import login,authenticate,logout
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from validate_email import validate_email 



# Create your views here.
def home(request):
    
    return render(request, 'home.html')


def signup(request):
    if request.method =="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = request.POST.get('email')
            verify_email = validate_email(email = email , check_mx= True)
            if verify_email:
                user = authenticate(username=username, password=password)
                login(request, user , backend='django.contrib.auth.backends.ModelBackend')
                user_db =  User(username=username,password=password,email= email, date_created = datetime.now() , verified = False)
                user_db.save()
                messages.success(request, "Registration successful..")
                return redirect('home')
            else:
                messages.error(request,"Invalid email address.")
        messages.error(request," Unsuccessful registration . Invalid Information")
    form = SignUpForm
    return render(request, 'signup.html', {'form': form})
    

def signin(request):
    if request.method == "POST":
        form =  AuthenticationForm(request , data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username , password = password)
            if user is not None:
                login(request,user)
                messages.info(request,  f"You are now logged in as {username}.")
                return render(request,'profile.html')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, 'login.html' , {'form' : form})

def signout(request):
    logout(request)
    messages.info(request , "You have successfully logged out.")
    return redirect('home')
    