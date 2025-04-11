from django.shortcuts import render,redirect,get_object_or_404
from expert.models import Community
from pcod_finder.models import Usertable
from user.models import Comminityjoin  # Ensure this matches the model name

# Create your views here.

def community_members_view(request, community_id):
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

    return render(request, 'community_members_admin.html', {'members': member_data, 'community_id': community_id})


def admin_dash(request):
    return render(request,'admin_dash.html')

def permission_community(request):
    # Fetch all pending community requests
    communities = Community.objects.all()

    # Render only if there are records, else pass an empty list
    return render(request, 'permission_com.html', {'communities': communities})

def approve(request, id):
    # Get the community request by ID and update its status
    community = get_object_or_404(Community, id=id)
    community.status = "1"  # Assuming "1" means approved
    community.save()
    
    return redirect('permission_community')  # Redirect back to the list

def list_users(request):
    users = Usertable.objects.all()  # Fetch all users
    return render(request, 'list_users.html', {'users': users})

def delete_user(request, user_id):
    user = Usertable.objects.get(id=user_id)
    user.delete()
    return redirect('list_users')  # Redirect to updated user list
