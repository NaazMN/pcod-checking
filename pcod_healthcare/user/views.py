from django.shortcuts import render,redirect
from pcod_finder.models import Usertable,Expert_details
from expert.models import Community
from .models import Comminityjoin,Communitychatbox
from .models import Message
from django.db.models import Q
from django.utils.timezone import now


# Create your views here.
def home(request):
    return render(request, 'home_page.html')
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


def list_community_user(request):
    user_id = request.session.get('user_id')  # Get user_id from session

    if not user_id:
        return render(request, 'list_community.html', {'error': 'User not logged in'})

    communities = Community.objects.filter(status=1)
    community_data = []

    for community in communities:
        # Get the owner's name using the userid field
        owner = Usertable.objects.filter(id=community.userid).first()
        owner_name = owner.name if owner else "Unknown"

        # Check if the user is in the Communityjoin table
        comm_join = Comminityjoin.objects.filter(userid=user_id, comminityid=community.id).first()

        if comm_join:
            a_status = comm_join.a_status  # If found, get actual a_status
        else:
            a_status = 0  # If not found, return 0

        community_data.append({
            'id': community.id,
            'community_name': community.name,
            'type': community.Type,
            'owner_name': owner_name,
            'a_status': a_status
        })

    return render(request, 'list_community.html', {'communities': community_data})



def join(request, id):  # 'id' is the community ID
    user_id = request.session.get('user_id')  # Get user_id from session

    if not user_id:
        return redirect('list_community_user')  # Redirect if user is not logged in

    # Check if the user is already in the community
    existing_entry = Comminityjoin.objects.filter(userid=user_id, comminityid=id).first()

    if not existing_entry:  # Insert only if no existing entry
        Comminityjoin.objects.create(userid=user_id, comminityid=id, a_status=1)

    return redirect('list_community_user')  # Redirect back to community list
    





def community_chat(request, community_id):
    user_id = request.session.get('user_id')  # Get user ID from session
    
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            # Insert message into Communitychatbox
            Communitychatbox.objects.create(
                userid=user_id,
                comminityid=community_id,
                message=message_text,
                a_status=1  # Assuming 1 means active message
            )
    
    # Fetch all messages for this community
    messages = Communitychatbox.objects.filter(comminityid=community_id).order_by('id')

    chat_data = []
    for msg in messages:
        sender = Usertable.objects.filter(id=msg.userid).first()
        chat_data.append({
            'name': sender.name if sender else "Unknown",
            'message': msg.message,
            'is_self': msg.userid == user_id  # Check if the message is from the logged-in user
        })

    return render(request, 'community_chat.html', {'community_id': community_id, 'chat_data': chat_data})


def community(request):
    user_id = request.session.get('user_id')  # Retrieve user ID from session

    if not user_id:
        messages.error(request, "User is not logged in!")
        return redirect('login')  # Redirect to login if user ID is missing

    if request.method == 'POST':
        communityName = request.POST.get('communityName')
        communityDescription = request.POST.get('communityDescription')
        communityType = request.POST.get('communityType')
        communityRules = request.POST.get('communityRules')

        if not communityName or not communityDescription or not communityType or not communityRules:
            messages.error(request, "All fields are required!")
            return redirect('community')  # Redirect to the same page

        try:
            new_community = Community.objects.create(
                userid=user_id,
                name=communityName,
                description=communityDescription,
                Type=communityType,
                Rules=communityRules,
                status="Pending"  # Default status
            )
            messages.success(request, "Community registered successfully!")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    # Fetch all communities for the logged-in user
    user_communities = Community.objects.filter(userid=user_id)  

    context = {
        'user_communities': user_communities
    }

    return render(request, 'community_reg.html', context)