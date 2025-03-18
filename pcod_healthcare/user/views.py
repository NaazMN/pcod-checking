from django.shortcuts import render,redirect
from pcod_finder.models import Usertable,Expert_details
from .models import Message
from django.db.models import Q


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
                'userid': user.id,
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

def chatsystem(request, doctor_id):
    # Get the doctor information
    doctor = Usertable.objects.get(id=doctor_id)
    
    # Get or create a chat session between user and doctor
    user_id = request.session['user_id']
    
    # Get existing messages
    messages = Message.objects.filter(
        (Q(sender_id=user_id) & Q(receiver_id=doctor_id)) |
        (Q(sender_id=doctor_id) & Q(receiver_id=user_id))
    ).order_by('timestamp')
    
    # Process new message submission
    if request.method == 'POST':
        message_text = request.POST.get('messagebox')
        if message_text:
            # Create and save new message
            new_message = Message(
                sender_id=user_id,
                receiver_id=doctor_id,
                content=message_text
            )
            new_message.save()
            
            # Redirect to avoid form resubmission on page refresh
            return redirect('chat_system_box', doctor_id=doctor_id)
    
    context = {
        'doctor': doctor,
        'messages': messages,
        'user_id': user_id
    }
    
    return render(request, 'doctor-chat-box.html', context)