from django.shortcuts import render
from pcod_finder.models import Usertable,Expert_details

# Create your views here.

def user_dashboard(request):
    return render(request,'dashboard.html')


def chatapp(request):
    # Get all users with usertype=1
    basic_details = Usertable.objects.filter(usertype=1)
    
    # Get all expert details for the corresponding users
    expert_details = Expert_details.objects.filter(userid__in=basic_details.values_list('id', flat=True))
    
    # Create a list of dictionaries with combined data
    doctors_data = []
    for user in basic_details:
        # Find matching expert details
        expert = expert_details.filter(userid=user.id).first()
        if expert:
            doctors_data.append({
                'userid': str(user.id),
                'name': user.name,
                'email': user.email,
                'phoneno': user.phoneno,
                'Specialization': expert.Specialization,
                'Experience': expert.Experience,
                'Medical_License': expert.Medical_License,
                'Educational_Qualifications': expert.Educational_Qualifications
            })
    
    # Pass the combined data to the template
    return render(request, 'communication-page.html', {'details': doctors_data})

