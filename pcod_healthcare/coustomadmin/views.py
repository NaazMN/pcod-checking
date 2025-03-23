from django.shortcuts import render,redirect,get_object_or_404
from expert.models import Community

# Create your views here.


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
