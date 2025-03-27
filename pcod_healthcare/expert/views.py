from django.shortcuts import render,redirect
from pcod_finder.models import Usertable
from user.models import Message
from django.db.models import Q
from django.contrib import messages
from .models import Community
from user.models import Comminityjoin  # Ensure this matches the model name



# Create your views here.

def exper_dashboard(request):
    # Get user_id from the session
    user_id = request.session.get('user_id')

    return render(request, 'simple-expert-dashboard.html', {'user_id': user_id})


def message_inbox(request):
    # Get the current user from session
    user_id = request.session['user_id']
    
    # Get all users who have messaged the current user
    message_senders = Message.objects.filter(
        receiver_id=user_id
    ).values('sender_id').distinct()
    
    # Prepare data for template
    conversations = []
    
    for sender in message_senders:
        sender_id = sender['sender_id']
        
        # Get sender's user info
        try:
            sender_user = Usertable.objects.get(id=sender_id)
            
            # Count unread messages from this sender
            unread_count = Message.objects.filter(
                sender_id=sender_id,
                receiver_id=user_id,
                is_read=0  # Assuming you have an is_read field in Message model
            ).count()
            
            # Get the latest message for preview
            latest_message = Message.objects.filter(
                (Q(sender_id=user_id) & Q(receiver_id=sender_id)) |
                (Q(sender_id=sender_id) & Q(receiver_id=user_id))
            ).order_by('-timestamp').first()
            
            conversations.append({
                'sender': sender_user,
                'unread_count': unread_count,
                'latest_message': latest_message
            })
            
        except Usertable.DoesNotExist:
            # Handle case where user no longer exists
            pass
    
    context = {
        'conversations': conversations,
        'user_id': user_id
    }
    print(context)
    return render(request, 'chat.html', context)





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



def list_community(request):
    """ Fetch all communities with owner details """
    user_id = request.session.get('user_id')
    communities = Community.objects.exclude(userid=user_id).all()
    community_data = []
    for community in communities:
        # Get the owner's name using the userid field
        owner = Usertable.objects.filter(id=community.userid).first()
        owner_name = owner.name if owner else "Unknown"

        community_data.append({
            'id': community.id,
            'community_name': community.name,
            'type': community.Type,
            'owner_name': owner_name
        })

    return render(request, 'list_community.html', {'communities': community_data})


def list_community_mine(request):
    """ Fetch all communities with owner details """
    user_id = request.session.get('user_id')
    communities = Community.objects.filter(userid=user_id).all()

    community_data = []
    for community in communities:
        # Get the owner's name using the userid field
        owner = Usertable.objects.filter(id=community.userid).first()
        owner_name = owner.name if owner else "Unknown"

        community_data.append({
            'id': community.id,
            'community_name': community.name,
            'type': community.Type,
            'owner_name': owner_name
        })

    return render(request, 'list_communitymine.html', {'communities': community_data})


def community_members(request, community_id):
    # Get all users who joined the community
    members = Comminityjoin.objects.filter(comminityid=community_id)

    member_data = []
    for member in members:
        user = Usertable.objects.filter(id=member.userid).first()
        if user:
            member_data.append({
                'name': user.name,  # User name from Usertable
                'a_status': member.a_status,  # Approval status from Comminityjoin
                'join_id': member.id  # ID of Comminityjoin entry
            })

    return render(request, 'community_members.html', {'members': member_data, 'community_id': community_id})


def approve(request, join_id):
    # Find the entry in Comminityjoin by ID
    comm_join = Comminityjoin.objects.filter(id=join_id).first()

    if comm_join:
        comm_join.a_status = 2  # Update a_status to 2 (Approved)
        comm_join.save()  # Save the changes

    return redirect('community_members', community_id=comm_join.comminityid) 