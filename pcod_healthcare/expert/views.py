from django.shortcuts import render

# Create your views here.

def exper_dashboard(request):
    
    return render(request,'simple-expert-dashboard.html')
