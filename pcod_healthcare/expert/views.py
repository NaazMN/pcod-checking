from django.shortcuts import render
from pcod_finder.models import Usertable
from user.models import Message
from django.db.models import Q


# Create your views here.

def exper_dashboard(request):
    
    return render(request,'simple-expert-dashboard.html')


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
