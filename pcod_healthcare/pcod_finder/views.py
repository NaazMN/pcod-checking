from django.shortcuts import render
# Create your views here.
from . models import Usertable

def print_hello(request):
    return render(request,'home_page.html')

def register(request):
    if request.POST:
        name=request.POST.get('firstName')
        lname=request.POST.get('lastName')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        dob=request.POST.get('dateOfBirth')
        gender=request.POST.get('gender')
        password=request.POST.get('password')

        usertable_Obj = Usertable(name=name,lname=lname,email=email,phoneno=phone,dob=dob,gender=gender,password=password)
        usertable_Obj.save()
    return render(request,'user_registration.html')